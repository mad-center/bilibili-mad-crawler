# 多线程并行请求

实现多线程并行请求本身并没有太大的难度。

- 使用线程池，合理设置池参数，定义任务function。
- 将任务function提交到线程池，线程池会自动管理它自身的线程分配。

## 实现

### concurrent

concurrent.futures.ThreadPoolExecutor()

- executor.submit(request_post, url, payload)
- futures.wait()
- for loop res, use response.result() to get real response

### threading.Semaphore

```python
# 初始信号量，作为并发度，这里是2
lock = threading.Semaphore(2)

# 创建线程，将线程放入池，启动线程
thread = threading.Thread(target=parse, args=(url,))
thread_pool.append(thread)
thread.start()

# 获取一个锁，也就是信号量-1
# 原文：If it is zero on entry, block, waiting until some other thread has called release()
# to make it larger than zero.
lock.acquire()

# 每次处理完一个url后，释放一个锁，信号量+1
lock.release()

# 主线程等待所有线程完成
thread.join()
```

### asyncio

- 定义异步函数: async def parse(url)
- 等待解析完成: completed, pending = await asyncio.wait(parses)

主线程开启事件轮询，运行轮询直到完成。

```python
event_loop = asyncio.get_event_loop()
try:
    websites = ['site1', 'site2', 'site3']
    event_loop.run_until_complete(main(websites))
finally:
    event_loop.close()
```

### grequests

> grequests

### request-futures