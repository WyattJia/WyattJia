
Envoy 是一个面向 service mesh 的高性能网络代理，由 C++ 实现，性能基本持平 NGINX 。本文中我们会在本地环境快速上手使用 envoy 。了解一个开源软件，从官方实例入手再好不过了，因此下面的例子将会围绕官方仓库中的实例展开。


### 前提条件

* Docker
* Docker Compose
* Git
* curl

我们将会使用 Docker 和 Docker Compose 来构建和运行几个 Envoy 示例服务，并用 curl 来检测服务是否在运行。

### 运行 Envoy

首先克隆 Envoy 官方仓库到本地,并定位到 `envoy/examples/front-proxy` 文件夹。

```shell
git clone https://github.com/envoyproxy/envoy
cd envoy/examples/front-proxy

```


`front-proxy` 文件夹中的服务是一个用 Flask 实现的服务，入口文件在 `service.py` 文件里面。Envoy 作为一个 sidecar 部件，将与 `service.py` 在同一个容器中运行，并由 `docker-compose,.yaml` 文件配置。
`front-envoy.yaml` 文件配置了 envoy 的参数，`Dockerfile-frontenvoy` 文件则是 front-envoy 的 Dockerfile 。

如果你之前没有接触过 Docker 的话，你可以使用以下命令在本地构建并运行 front-proxy 的 Docker 镜像：

```shell
$ cd /path/to/envoy/examples/front-proxy
$ docker-compose up --build -d
```

`--build` 表示构建镜像， `-d` 表示在后台运行所有 docker-compose 配置文件中定义的镜像，具体可参考 docker 相关文档。

运行成功之后，你可以通过以下命令来验证容器是否正常运行:

```
$ docker-compose ps
```

正常的话会返回以下内容:

```shell
$ front-proxy git:(master) docker-compose ps
          Name                         Command               State                            Ports
----------------------------------------------------------------------------------------------------------------------------
front-proxy_front-envoy_1   /usr/bin/dumb-init -- /bin ...   Up      10000/tcp, 0.0.0.0:8000->80/tcp, 0.0.0.0:8001->8001/tcp
front-proxy_service1_1      /bin/sh -c /usr/local/bin/ ...   Up      10000/tcp, 80/tcp
front-proxy_service2_1      /bin/sh -c /usr/local/bin/ ...   Up      10000/tcp, 80/tcp
```

### 测试服务是否连通

你可以使用 curl 或者浏览器来测试服务是否在正常运行

浏览器中输入 [http://localhost:8000/service/1](http://localhost:8000/service/1) 或者使用以下命令:

```shell
curl localhost:8000/service/1
```

如果返回结果是像下面这样，则表示 `service1` 的 envoy 服务正常运行:

```shell
Hello from behind Envoy (service 1)! hostname: a841ffceafd0 resolvedhostname: 172.18.0.4
```

你也可以用同样的方法测试 service 2 的服务

打开 [http://localhost:8000/service/2](http://localhost:8000/service/2 )
返回 `Hello from behind Envoy (service 2)! hostname: e83b35c6f4fe resolvedhostname: 172.18.0.3` 。

### Envoy 配置

下面我们先简单看一下 envoy 的静态配置信息,之后再继续看 demo 中的动态配置信息。因为 docker 和 docker-compose 的配置不是我们的重点，所以我会略过 demo 中与此相关的内容。

我们先从 `front-envoy.yml` 入手。打开文件之后，我们会发现这个 yaml 有两个最高的层级，分别是 `static-resources` 和 `admin` 。`admin` 的内容相对比较简单，总共只有六行:


```yaml
admin:
   access_log_path: "/dev/null"
   address:
     socket_address:
       address: 0.0.0.0
       port_value: 8001
```

其中 `access_log_path` 字段值是 `/dev/null`，其含义是 admin 服务的请求日志将不会被保存。生产环境中可自行将目标目录指定到需要的地方。`address` 和 `port_value` 字段分别表示 admin server 运行的 ip 端口。

`static_resource` 的内容定义了非动态管理的集群和监听器相关配置。一个集群是一组被定义的 ip/port 集合，Envoy 将借此实现负载均衡，监听器是一组被定义的网络地址，客户端可借此连接至服务。 

front proxy 中只有一个监听器，监听器中除了 socket_address 之外还有一个字段是 `filter_chains`，Envoy 通过此字段来管理 HTTP 的连接和过滤。其中有个配置选项是 `virtual_hosts` ，通过正则过滤允许访问服务的域名。路由也在其中配置，例子中将 `/service/1` 和 `/service/2` 的请求分别转发到了其相应的集群中。

```yaml
virtual_hosts:
- name: backend
  domains:
  - "*"
  routes:
  - match:
      prefix: "/service/1"
    route:
      cluster: service1
  - match:
      prefix: "/service/2"
    route:
      cluster: service2

```


接下来我们继续看静态集群的配置:

```yaml
  clusters:
  - name: service1
    connect_timeout: 0.25s
    type: strict_dns
    lb_policy: round_robin
    http2_protocol_options: {}
    hosts:
    - socket_address:
        address: service1
        port_value: 80
  - name: service2
    connect_timeout: 0.25s
    type: strict_dns
    lb_policy: round_robin
    http2_protocol_options: {}
    hosts:
    - socket_address:
        address: service2
        port_value: 80

```

在静态集群的配置内容中，我们可以配置超时时间，熔断器，服务发现等等内容。集群由一系列端点(endpoints)组成，端点就是一组服务集群中可以响应访问请求的网络地址。在上面的例子中，端点标准定义成 DNS ，除此之外，端点可以直接被定义成 socket 地址，或者是可动态读取的服务发现机制。

### 尝试动手修改配置

我们可以在本地尝试自己修改配置，重建镜像，测试修改后的配置。监听过滤器是 Envoy 为监听器提供的附加功能。比方说，想要增加访问日志到我们的 HTTP 过滤器中，只要增加 `access_log` 字段到配置文件中即可:

```yaml
    - filters:
      - name: envoy.http_connection_manager
        config:
          codec_type: auto
          stat_prefix: ingress_http
          access_log:
            - name: envoy.file_access_log
              config:
                path: "/var/log/access.log"
          route_config:

```

修改之后，先通过 `docker-compose down` 命令关闭 docker-compose 容器组，然后使用 `docker-compose up --build -d` 命令重新构建镜像并运行容器组即可。为了验证我们新增的 `access_log` 字段是否生效，我们可以模拟几次请求之后，手动进入容器内部查看访问日志是否在相应的目录中。进入容器的命令可以用 `docker-compose exec front-envoy /bin/bash` 。

### 管理页面

Envoy 提供了自己的管理页面，你可以通过 http://localhost:8001 访问。

管理页面中 `/cluster` 菜单展示了上游(upstream)集群端口的统计内容，`stats` 菜单则显示了更多端口的统计内容。更多管理页面的内容你可以直接访问帮助页面 http://localhost:8001/help 来查看。

### 进一步了解

#### 服务发现

如果你想进一步了解 envoy 的话, `example` 文件夹中其实还有好几个可供参考的例子，你可以挨个研究，但是这些例子都只是静态集群。如果想要了解 Envoy 在生产环境运行的配置，可以了解一下官方文档中有关动态服务发现相关的内容: [service\_dicovery](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/service_discovery)

#### 请求处理

Envoy 中对访问请求的处理流程大致如下，先将请求数据预处理，转成 Envoy 中的 `Filter`， 读写请求的 filter 分别是 `ReadFilter` 和 `WriteFiler`，对每个网络层也有各自的 filter ，TCP 的是 TcpProxyFilter, HTTP 的是 ConnectionManager，都由读 filter `ReadFilter` 继承而来。各个 filter 预处理完成之后就会组织成上面示例配置文件中有提到的 `FilterChain`， 收到 `FilterChain`
之后会将其路由到指定的集群中，并根据负载均衡获取到相应的地址，然后将请求转发出去。

#### 事件模型

Envoy 采用的是跟 NGINX 类似的非阻塞多线程异步IO的架构，因此性能上不会太差。

#### 与 NGINX 的区别

* Envoy 对 HTTP/2 的支持比 NGINX 更好，支持包括 upstream 和 downstream 在内的双向通信，而 NGINX 支持 downstream 的连接。
* 高级负载均衡功能是免费的:)。NGINX 的高级负载均衡功能则需要付费的 NGINX Plus 支持。
* Envoy 支持热更新，NGINX 配置更新之后需要reload
* Envoy 更贴近 service mesh 的使用习惯，NGINX 更贴近传统服务的使用习惯
