`fcntl` 提供了 Python 文件锁的支持，实际上就是 Unix 的 `ioctl`、`flock` 和 `fcntl` 接口的一层封装。

linux 的 flock() 接口如下:

```c
int flock(int fd, int operation);
```

函数参数中的 `fd` 就是 file description 的缩写，`operation` 参数就是指定锁的操作。`operation` 的参数选项如下:

* `LOCK_SH`: SH 就是 share 的缩写，其表示创建一个共享锁，即一个文件的共享锁可以在任意时间内被任意多个进程使用。

* `LOCK_EX`: EX 是 except 的缩写，表示创建一个排他锁，即一个文件的排它锁在任意时间内只能被一个进程使用。

* `LOCK_UN`: UN 大概是 undo 的缩写，其表示撤销该进程创建的锁。

* `LOCK_MAND`: MAND 缩写未知，主要用于创建共享模式的强制锁，通常会与 `LOCK_READ` 和 `LOCK_WRITE` 搭配使用，表示是否允许并发的读操作或者写操作。

通常情况下，如果加锁操作不能被立即执行，那么系统调用 `flock()` 函数来进行加锁操作会阻塞当前进程。例如，进程想要请求一个文件的排它锁，但是请求的时候，已经有其他进程获取了这个锁，那么加锁请求不会被满足，该进程就会被阻塞（超时 or exception ?）。如果想要在没有获得这个排它锁的情况下不阻塞该进程，可以将 `LOCK_NB` 和 `LOCK_SH` 或者 `LOCK_EX` 联合使用，那么系统就不会阻塞该进程。flock()所加的锁会对整个文件起作用。


### Example

```python

import os
import time
import uuid
import fcntl


FILE = "test.txt"


if not os.path.exists(FILE):
    file = open(FILE, 'w')
    text_line = 'bitstring.xyz.   300  IN  A  97.64.39.196'
    file.write(text_line + '\n')
    file.close()


for i in range(5):
    file = open(FILE, "a+")
    fcntl.flock(file.fileno(), fcntl.LOCK_EX)
    print('scquire lock')
    now_port = int(file.readline()[-1].split(':')[-1])
    new_port = now_port + 1
    token = str(uuid.uuid4())
    # file.seek(0)
    text_line = ":".join([token, '127.0.0.1', str(new_port)])
    file.write(text_line + '\n')
    print(os.getpid(), '=>', new_port)
    time.sleep(10)
    file.close()
    print('release lock')
    time.sleep(2)
```
