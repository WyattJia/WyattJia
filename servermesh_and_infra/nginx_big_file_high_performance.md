## 

### `sendfile on`


* `sendfile 	on | off;` 
       * 开启高效文件传输模式
       * 放置位置 `http` `server` 	`location` `if in location`

 * `tcp_nopush	  on | off;` 
      * 有数据的时候，先不着急发送，确认数据包装满数据再发送，避免网络阻塞。仅开启 `sendfile on` 时有效。
      * 放置位置 `http` `server` `location`
      * 内部作用: 激活或者禁用 Linux 上 `TCP_CORK ` socket 选项，该选项的作用是接收到数据包之后不会马上传出去，等到数据包最大时再传送，可以减少网络报文段的数量

 * `tcp_nodelay		on | off;`  
       * 有数据时要尽快发送，提高数据传输效率
       * 放置位置 `http` `server` `location`
       * 作用：激活或禁用 `TCP_NODELAY` 选项，只有在连接进入 `keep-alive` 状态时生效。`TCP_NODELAY` 和 上面提到的 `TCP_CORK` 控制了数据包中的 `Nagle` 化，目的是采用 `Nagle` 算法将较小的包组装为更大的帧，以减少网络阻塞。


**sendfile on** 通常配合上面的 2, 3选项使用，但是两者之中只能选一个生效。

  * example:
      ```nginx
      worker_processes  2;
      worker_cpu_affinity 0101 1010;
      error_log logs/error.log;

      #配置Nginx worker进程最大打开文件数
      worker_rlimit_nofile 65535;

      user www www;
      events {
      #单个进程允许的客户端最大连接数
      worker_connections  20480;
      #使用epoll模型
      use epoll;
      }
      http {
      include       mime.types;
      default_type  application/octet-stream;
      #sendfile        on;
      keepalive_timeout  65;
      #访问日志配置
      log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
      '$status $body_bytes_sent "$http_referer" '
      '"$http_user_agent" "$http_x_forwarded_for"';


      #虚拟主机
      include /application/nginx/conf/extra/www.conf;
      include /application/nginx/conf/extra/blog.conf;
      include /application/nginx/conf/extra/bbs.conf;
      include /application/nginx/conf/extra/edu.conf;
      include /application/nginx/conf/extra/phpmyadmin.conf;
      include /application/nginx/conf/extra/status.conf;
      
      #nginx优化----------------------
      #隐藏版本号
      server_tokens on;
      
      #优化服务器域名的散列表大小 
      server_names_hash_bucket_size 64;
      server_names_hash_max_size 2048;
      
      #开启高效文件传输模式
      sendfile on;
      #减少网络报文段数量
      #tcp_nopush on;
      #提高I/O性能
      tcp_nodelay on;
      }  
   ```

---
---

### 调用 sendfile system call 接口，将文件作为包体发送

NGINX 响应用户请求的时候，如果用户请求的是磁盘上的文件，NGINX 将不会把文件读取到内存，再发送给用户，那样真的太费内存以及 IO 性能了。NGINX 的做法是，直接通过上文提到的 `sendfile` 接口，来调用 system call ，从而是文件请求在不经过 User space 的情况下，直接在 kernel space 发送出去，这样做无疑减少了 IO 性能和内存使用率，大大提高了性能。同时 NGINX 也提供了 sendfile 接口，供我们在更多的场景下高效率发送文件。

```c
/*ngx_buf_s 设置缓冲区*/
```

```c
/* ngx_file_t 表示一个文件*/
```

```c
/* ngx_pool_cleanup_s http 响应结束之后关闭 fd */
```

* example

```c
```

---
---


### XSendfile in X-Accel

saw [XSendfile](https://www.nginx.com/resources/wiki/start/topics/examples/xsendfile/)