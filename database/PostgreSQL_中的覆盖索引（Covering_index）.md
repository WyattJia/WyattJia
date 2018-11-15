数据库索引是在数据库中使用非常广泛的一个概念。索引就像是书的目录，通过书的目录能快速准确地定位到书籍的具体内容。
通常的关系型数据库中的索引数据结构都是由平衡树来维护的。一般我们给数据库建表的时候，都会为表指定一个主键。数据库正是根据表的主键将若干个表梳理成树状结构的。表中的主键也就相当于一个索引，也叫做聚集索引。数据库中的表顺序相对固定，一般只有一种顺序，通常就是由上面提到的平衡树来维护，平衡树中的叶节点都是由主键字段构成。因此，一般一张表只会有一个聚集索引。
假设我们执行一个 SQL 语句：

``` sql
SELECT * FROM people WHERE id = 1234;
```

数据库会根据聚集索引定位到 1234 所在的叶结点，然后再通过这个叶结点取到响应的数据行。这个查找分为三层，先从平衡树的根节点，也就是 dbs 开始查找，然后根据聚集索引找到对应 id=1234 的主键，即叶结点，最后是根据叶结点找到相关的数据行。
使用平衡树逐级去查找数据的速度，相比一条一条遍历查找的速度是以指数级提升的。
但是用了索引之后，虽然查找速度变快了，但是其插入数据却下降了。因为每次从平衡树插入新数据之后，平衡树都要自行‘平衡’一下，使树结构维持在一个正确的状态。增加删除更新数据都会改变平衡树中的索引结构，因此除了聚集索引之外我们还需要非聚集索引。

非聚集索引同样也是用平衡树来存储数据，区别在于非聚集索引中各个叶结点的数据来自于表中手动定义的索引字段，而非主键。假如说我们给 people 表中的 name 字段加上索引，那么 name 字段就会有自己的，区别于主键结构的一套非聚集索引结构了。

与聚集索引一样，因为平衡树结构的限制，每个索引都有自己独立的索引结构，也就是说每个索引都有自己的一个平衡树结构。比方说，上面的 name 字段有自己的结构，如果我们给 age 字段也加上索引，那么 age 字段也会有自己的结构， name 和 age
之间的所有结构不会相互影响。

每次给新字段增加一个索引，字段中的数据就会被复制出来，生成一份新的索引结构，因此给表加新索引的同时也会增加表的体积，会占用磁盘空间。

通过非聚集索引，我们可以会先查找到对应内容的索引字段，然后根>据找到的字段找到对应的主键值，再使用主键值通过聚集索引找到需> 要查找的数据。因此非聚集索引还是依赖聚集索引来定位数据的。但是除了这两种索引之外还有一种索引，叫做覆盖索引，就是今天要讲的那种索引。

覆盖索引英文名叫做 Covering index ，是 MySQL 中‘特有’的一种索引。不同于我上面提到的两种索引，它可以不依赖聚集索引就能找到所需要的数据。使用非聚集索引的时候，每当为一个字段建立索引之后，字段中的内容就会被同步到索引结构中，如果为一个索引指定了两个字段，那么这两个字段的内容都会被同步到索引中。

看一下这个例子:

```sql
// 构建索引
CREATE index index_birthday ON user_info(birthday);

// 查询内容
SELECT user_name FROM user_info WHERE birthday='1993'
```

这个例子的执行过程如下，
* 先通过非聚集索引 index\_birthday 查找 1993 年出生的人所对应的主键值。
* 然后用得到的主键值通过聚集索引查找，找到对应的数据行
* 最后，从得到的数据行中得到需要的 user\_name 字段的值返回。

假设我们把 index\_birthday 索引改为覆盖索引：

```sql
CREATE index index_birthday_and_user_name ON user_info(birthday, user_name);
```

这个例子的执行过程变为：

* 通过 index\_birthday\_and\_user\_name 这个索引找到 1993 年出生的叶结点
* 叶结点中除了有需要查找的主键值之外，也包含了 user\_name 字段的值，因此直接取出 user\_name 对应的值即可。

可以看到，用了覆盖索引比没用覆盖索引少了两个步骤，比较快。

但是，这么方便的东西难道只有 MySQL 用户才能体验到？让我们这些使用 PostgreSQL 的用户情何以堪 :doge
不信邪的我 Google 了一番，发现了 psql wiki 里面这么一段[文字](https://wiki.postgresql.org/wiki/Index-only_scans#Covering_indexes)：

```
Covering indexes
Covering indexes are indexes creating for the express purpose of being used in index-only scans. They typically "cover" more columns than would otherwise make sense for an index, typically columns that are known to be part of particular expensive, frequently executed query's selectlist. PostgreSQL supports using just the first few columns of the index in a regular index scan if that is in the query's predicate, so covering indexes need not be completely
useless for regular index scans.
```

大致意思就是 psql 有个叫做 index\_only scans 的东西，支持在创建索引的时候，包括一些查询语句中的字段，因此只要提取到对应的索引中的字段就行了，不需要再去查找数据行中的内容。这应该就是 psql 中的覆盖索引实现了，只是换了个名字。使用 index\_only scans 的时候会有两个限制：

* 索引类型必须支持 index\_only scans 的查找
* 只能查询存储于索引中的列。

除此之外，wiki 中还提到一句话:

> But there is an additional requirement for any table scan in PostgreSQL: it must verify that each retrieved row be "visible" to the query's MVCC snapshot, as discussed in Chapter 13.

意思大致是还有一个额外的限制，必须验证每个检索到的行对于该查询的 MVCC 快照是可见的。可见性信息并不存储在索引项中，只存储在堆项中。因此经常会发生从索引中找到数据，还要去数据堆中查找数据可见性的情况，还是有点耗费性能。但是 psql
提供了一个功能，它可以为表堆中的每一个页面跟踪是否其中所有的行的年龄都足够大，以至于对所有当前以及未来的事务都可见。这个信息存储在该表的可见性映射的一个位中。在找到一个候选索引项后，index\_only scans 会检查对应堆页面的可见性映射位。
因此对于那些不常更新的表可能会更加适用 index\_only scans 。

创建索引的时候，在语句末端加上需要的字段即可创建:

``` sql
CREATE INDEX idx_pings_monitor_created
ON pings (monitor_id, created_at DESC, response_time)
WHERE response_time IS NOT NULL;
```

上面的例子创建了一个包含了 monitor\_id, created\_at, response\_time 字段，位于 pings 表，并且 response\_time 不为空的叫做 idx\_pings\_monitor\_created 索引。

