## What is io_uring

自从 Linux 2.5 发布，其内核已经支持异步 I/O （AIO），但是自 AIO 发布以来，人们也抱吐槽了相当长一段时间 AIO 是多么的难用，效率低下。这个情况可能随着 linux 5.1 中的 io_uring 的发布而终结。
io_uring 是 Jens Axboe 提出的，用于代替原先 AIO 的接口，Linux 5.1合入的一个新的异步IO框架和实现。其主旨是在 Linux 上实现更加快速，更加高效的异步 I/O 操作。

## Why io_uring

io_uring 的效率远远超过之前的异步I/O (AIO) ，它有更加高效的缓冲支持。
相比 AIO ，io_uring 的优点有：
* 更加简单易用: io_uring 仅仅提供了三个系统调用来处理  I/O，分别是 `io_uring_setup`、`io_uring_register` 以及 `io_uring_enter`
* 更高的可扩展性
* 特性丰富，适用性广
* 更加高效： 顾名思义，io_uring 给内核加入了一对叫做 ring buffer 的 io 缓冲区，用于在用户态和内核态之间的通信，从而避免在提交事件和完成事件的时候发生多余的内存拷贝。
* 更强的可伸缩性。
* 通过 io_uring 提供的系统调用，应用程序可以使用两个 Queue（Submission queue，Completion queue） 来与 kernel 进行通信，可以高效处理 I/O 。
* 通过上面提到的两个队列， I/O 事件的提交和完成可以直接由 kernel 层完成，而不需要经由用户态应用调用 system call 之后，再将 I/O 事件交由 kernel 处理。
    
    测试 per-core，4k randread 多设备下的最高 IOPS 能力：
    *数据来源于 Jens Axboe 本人*
   ```text
   Interface       QD      Polled          IOPS
   --------------------------------------------------------------------------
   io_uring        128     1               1620K
   libaio          128     0                608K
   spdk            128     1               1739K
 ``` 

    使用了 polling 模式的 io_uring 速度已经接近 kernel bypass 的 spdk ,同时也完全超越了上一代 linux async io AIO 了。

#### Example

1.  poll 单个 fd :
```c
static inline void io_uring_prep_poll_add(
    struct io_uring_sqe *sqe, 
    int fd, 
    short poll_mask);
```
2. poll 多个 fd:

*to be continue...*

