1. SLA 
  service level agreements 服务级别协议，服务间达成承诺的服务指标。 
  包括以下几项指标:
  * 可用性
  * 精确性
  * 容错性
  * 响应时间

2. 垂直扩展与水平扩展
  * 水平扩展，就是加机器，更流行的做法。
  * 垂直扩展，买更加强大的机器。

3. 一致性
  可用性  Goal: down 5 min/year. 简单粗暴的一种办法就是加更多的机器。
  常用的一致性模型:
     * 强一致性
     * 弱一致性
     * 最终一致性（弱一致性的一种特例）

4. 数据持久化
  * machine/node 层级的持久化，位于集群内部
  * 复制集的自我增长，集群级别的持久化

5. 消息队列的高可用和持久化

6. 幂等性
   重试请求，结果一致

7. 分片和 quorum

8. Actor model
   提高分区容错性

9. 弹性架构
   * (Reactive Manifesto)[https://www.reactivemanifesto.org/] 中文[反应式宣言](https://www.reactivemanifesto.org/zh-CN)
   * (Understand reactive architecture design and programming in less than 12 minutes)[https://www.lightbend.com/blog/understand-reactive-architecture-design-and-programming-in-less-than-12-minutes]

---

原文: https://blog.pragmaticengineer.com/distributed-architecture-concepts-i-have-learned-while-building-payments-systems/

  
