## 这篇文章需要一些 linux 内核内存管理子系统的前提知识准备

最近我们在生产环境遇到一个 OOM 的问题。我们的工程师发现，slab 缓存一直不断的在增加，但是 page cache 却在一直减少。通过进一步观察发现，消耗 slab 内存最多的是 dentry cache（怎么理解 dentry cache ？），dentry caches 通过一个 内存 cgroup 来补充。这看起来像是 linux kernel 内存回收器只会回收 page cache ，而不会回收 dentry cache 的原因。

于是我们尝试通过这条命令来清理 slab 缓存

```shell
# echo 2 > /proc/sys/vm/drop_caches
```

但是出乎意料的是，这条命令似乎并没有成功清理掉缓存。

通过调试这个问题，我们发现了一个shrinker 代码里存在一个竟态条件的问题。

### 背景
为了充分理解是什么阻碍了 slab cache 的清楚，我们需要预先了解 linux kernel 内部机制，
更加细致了解内存管理子系统。
