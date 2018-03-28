## 为什么使用服务发现

使用 restful 或者 thrift api 调用某些服务。为了发送请求，代码层面需要知道服务的网络地址（端口 + IP）。传统应用运行在物理网络上，网络地址相对静态，调用方只需要从配置文件读取服务网络地址即可。

微服务体系下与传统应用有较大区别。参见下图
[](https://cdn-1.wp.nginx.com/wp-content/uploads/2016/04/Richardson-microservices-part4-1_difficult-service-discovery.png)
