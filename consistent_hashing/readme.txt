~ 哈希一致性 Python 语言实现

  ~ 关键抽象

    * Entry 放入 cache 服务器中的对象
    * Server 真正放入缓存对象的 cache 服务器
    * Cluster 服务器集群。（假设会维护一组服务器，这相当于是一组服务器的代理，接受 put, get 请求，通过一定算法（普通取余或者哈希一致性将请求转发给特定的 server ）
