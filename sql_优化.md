
## 数据库变动/迁徙时需要注意的一些事

### The good

**能够在迁移数据库时安全操作数据库而不会导致宕机的操作。**

| 能够做的 |
| ----------- |
| 新增一个 column |
| 删除一个 column |
| concurrently 地增加一个索引 |
| 删除一个约束 (例如, 非可空选项) |
| 给现存的 column 增加一个默认值 |

---
---

### The bad

**不可取的一些办法，以及变通方法。**

| 不能在一个大 table 下做的操作         |    解决方法     |
| ------------------------------------- | :-------------: |
| 增加一个索引                          |  增加索引的时候加 CONCURRENTLY 关键词 | 
| 改变一个 column 的类型                |  新增一个新的 column, 更改代码以同时写入两个 column，然后将新的 column 回填至与旧 column 一样的量级。|
| 增加一个 column 的默认值              |  新增一个 column , 在一个分开的命令里设置默认值，然后将默认值填到 column 。 |
| 增加一个非空的 column                 |  新增一张带了非可空 column 的 table，同时写入两张 table ，逐渐将旧表数据回填到新表，然后切换到新表。[1] |
| 给一个 column 增加唯一约束            |  新增 column, concurrently 地添加唯一索引约束,然后给表增加约束。 [2] |
| 用 VACUUM FULL 清空磁盘工具 [3]           |  也可以使用 pg\_repack 代替 |


* [1] 

  解决方案较为繁琐，一般不太经常使用。建议在新键表的时候仔细点，搞清楚哪些字段需要设置成非空。

* [2] 
  ``` sql
  CREATE UNIQUE INDEX CONCURRENTLY token_is_unique ON large_table(token); 
  ALTER TABLE large_table ADD CONSTRAINT token UNIQUE USING INDEX token_is_unique;
  ```

* [3]
  删除一个 column 很快，但是 pg 并不会马上就从磁盘清除空间，除非调用 `VACUUM FULL` 命令，或者使用第三方工具 `pg_repack` 替代。
