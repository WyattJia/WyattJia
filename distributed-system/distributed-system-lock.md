### 分布式锁
对数据被外界修改保守态度，将数据锁定，不允许其他用户修改。

实现方案:
  * lamport barkery 面包店策略 （Redis 常用方案）
  * paxos
  * 乐观锁，根据数据库版本 version 区分。
