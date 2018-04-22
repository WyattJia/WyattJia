用过 NGINX 的人都知道，NGINX 的 `proxy_pass` 模块用作反向代理，可以转发请求到 URL 参数到指定的服务器上。
如：
```nginx
server {
    location / {
        proxy_pass http://192.168.0.1; 
        }}
```

示例中将 server 根目录的请求转发到了服务器 `192.168.0.1` 上。

受限于 HTTP 协议无状态的特点，有时候只靠转发 url 请求是没办法携带足够的数据到服务器的。然后人们发明了 cookies 来解决相关问题，我们可以通过 `cookies` 在客户端存储一定的数据，每次用户请求的时候自动在头部带上 cookies 的数据，使用 cookies 在一定程度上能够缓解 HTTP 无状态的‘弊端’。
然而，客户端往往并不是直接和服务器通信，中间还会经过反向代理以及负载均衡。有可能向 A 服务器发送了一个请求，但是 A 服务器只是一个中转服务，中转之后这个请求是被 B 服务器或者 C 服务器去处理，中间会跨几次域, 不同域之间的 cookies 的实现标准也不一定会一致，因此跨域通过 `proxy_pass` 转发请求的时候， cookies 很有可能会失效。
浏览器也会对 cookies 做一些限制，比如说，cookies 中的 domian 需要和当前访问页面的 domian 匹配，否则将无法写入 cookies 。如果请求 A 服务器 ，服务器用 proxy\_pass 将请求转发到了 B 服务器下，B 服务器处理请求之后返回了带有 `Domain=B` 的 cookies ，但是由于现在访问的页面还是在 A 服务器的域名下，因此 B 返回的 cookies 将不会被正常写入。

那么有没有办法在反向代理转发 url 请求的同时，能够同时转发重写 cookies 中的 domian ，使之能够被不同域的浏览器和服务器能够正常读写呢？
答案是有的。

NGINX 的 `ngx_http_proxy_module` 模块中有个指令  [proxy\_cookie\_domain](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cookie_domain) 可以实现这个功能。它可以通过正则将 cookies 中的 domain rewrite 别的 domian 。

语义如下：
``` nginx
Syntax:     proxy_cookie_domain off;
            proxy_cookie_domain domain replacement;
Default:    proxy_cookie_domain off;
Context:    http, server, location
```

比如说，我们想在 a.xxx 这个域名上从 b.xxx 获取 cookies ，我们可以写成这样:

```nginx
server {
    listen a.xxx:80;

    location /(.*) {
        proxy_cookie_domain a\.xxx b\.xxx;
        proxy_pass http://b.xxx;
        }
    }
```

与 `proxy_cookie_domain` 对应的还有一个 [proxy\_cookie\_path](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cookie_domain) 指令支持转发请求的时候重写 cookie 的 path 参数。

