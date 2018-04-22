* `concurrent.futures.ProcessPoolExecutor`
  属于 [concurrent.futures.Executor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor) 的一个子类，它会生成一个进程池，可以被异步调用。ProcessPoolExecutor 使用了 multiprocessing 模块来实现功能。可以用来规避计算密集或者耗时任务中的 GIL 问题。进程池只能接受和返回序列化的对象。进程总数不会超过 `concurrent.futures.ProcessPoolExecutor(max_workers=None)` 参数中的 `max_workers` 值。

简单的例子：

```python
import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

if __name__ == '__main__':
    main()
```

定义一个 `is_prime` （假装是计算密集型任务）函数判断是不是素数，给定一个数组 `PRIMES` , `main` 函数将 `is_prime` 函数和数据扔进进程池，并打印出函数结果。简单好用。

`ProcessPoolExecutor` 比较适合计算密集型和耗时长的任务，如果对任务执行要求高的话推荐使用更加全面的 rq 或者 celery 。

---

* `concurrent.futures.ThreadPoolExecutor`

`ThreadPoolExecutor` 与 ProcessPoolExecutor 一样，都是来自于自带的 `concurrent.futures` 包。属于 Python 自己提供的几个并发方案之一， `futures` 的意思是未完成的意思，应该指的是解决异步任务的几个方案。
顾名思义，与进程池不同的是 `ThreadPoolExecutor` 是线程池解决方案。他同样也是 Executor 的一个子类，因此进程池和线程池的调用方式也很类似，线程池中的最大线程数由 `max_worker` 参数指定，大部分机器的默认值是5。当一个 调用的一个 Future 对象等待另一个 Future 对象时，有可能会发生死锁。

简单的例子：

``` python
import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
```

定义一个函数 `load_url` 用来载入一个网站， 给定几个网站 `URLS`, 提交函数 `load_url` 和 url 进线程池生成 future 对象作为 key ，url 作为 value ，生成字典 future_to_url ,从字典中依次取出完成的任务，并打印出任务结果。简单好用。

因为线程切换的性能相对进程来说更小，所以 `ThreadPoolExecutor` 会更加适合用于 IO 密集型小任务。当然，如果对异步任务要求高的话还是推荐 rq 或者 celery 。

---

* `loop = asyncio.get_event_loop; loop.run_in_executor`

`asyncio.get_event_loop.run_in_executor()` 是 asyncio 下的一个模块，但是它的执行器并不是用协程来实现的，而是通过协程在后台唤起了一个线程池或者进程池。 会在执行器中调用一个函数，可能会是在进程池也可能是线程池。默认情况下会是线程池。`run_in_executor()` 接受的参数应该是 `Executor` 实例，函数以及函数需要的参数。与线程池和进程池不同的是，`run_in_executor()` 函数不需要指定 `max_workers` 参数，它会使用系统给的默认值。

简单的例子:

``` python
import asyncio
from urllib.request import urlopen

@asyncio.coroutine
def print_data_size():
   data = yield from get_data_size()
   print("Data size: {}".format(data))

# Note that this is a synchronous function
def sync_get_url(url):
   return urlopen(url).read()

@asyncio.coroutine
def get_data_size():
   loop = asyncio.get_event_loop()

   # These each run in their own thread (in parallel)
   future1 = loop.run_in_executor(None, sync_get_url, 'http://baidu.com')
   future2 = loop.run_in_executor(None, sync_get_url, 'http://bitstring.xyz')

   # While the synchronous code above is running in other threads, the event loop
   # can go do other things.
   data1 = yield from future1
   data2 = yield from future2
   return len(data1) + len(data2)

loop = asyncio.get_event_loop()
loop.run_until_complete(print_data_size())
```

定义一个函数 `sync_get_url` 从 url 读取数据，定义一个异步函数 `get_data_size()` ，将 `sync_get_url` 放入线程池，并根据任务返回结果计算页面大小。定义一个异步函数 `print_data_size`，读取并打印 `get_data_size()` 的结果。 定义一个 asyncio 任务队列，将 `print_data_size` 放入协程队列，依次将已完成的 `print_data_size()` 函数取出。简单好用。

协程比线程更轻量，更适合于 IO 密集任务。
