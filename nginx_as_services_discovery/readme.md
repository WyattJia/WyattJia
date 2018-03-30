## 为什么使用服务发现

使用 restful 或者 thrift api 调用某些服务。为了发送请求，代码层面需要知道服务的网络地址（端口 + IP）。传统应用运行在物理网络上，网络地址相对静态，调用方只需要从配置文件读取服务网络地址即可。

微服务体系下与传统应用有较大区别。

> 参见下图

![](./Richardson-microservices-part4-1_difficult-service-discovery.png)

看起来非常 'dynamically'

## 客户端（调用方）服务发现模式

当使用客户端服务发现模式的时候，有调用方来决定可用服务的地址，然后通过负载均衡来访问服务。调用方会查找一个服务注册表，表中存着可正常使用的服务实例列表。客户端会使用负载均衡算法来选择其中的一个可正常使用的服务实例来做请求。

> 见下图

![](./Richardson-microservices-part4-2_client-side-pattern.png)
