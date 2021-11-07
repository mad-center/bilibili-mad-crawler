# 多线程并行请求

实现多线程并行请求本身并没有太大的难度。
- 使用线程池，合理设置池参数，定义任务function。
- 将任务function提交到线程池，线程池会自动管理它自身的线程分配。

但是，爬虫由于容易出错。多线程任务的恢复成了一个难点。

为简化说明，这里假设线程池有5个固定线程大小。页数为16000。
那么将页数按段为5个范围;
- 分段1：1-3000
- 分段2：3001-6000
- 分段3：6001-9000
- 分段4：9001-12000
- 分段5：12001-16000

对于每个分段，各需要一个变量来记录当前分段的进度。例如
- 分段1：1-3000 | 当前进度 30
- 分段2：3001-6000 | 当前进度 5000
- 分段3：6001-9000 | 当前进度  7001
- 分段4：9001-12000 | 当前进度 9876
- 分段5：12001-16000  | 当前进度 14902

这样，无论程序如何出异常，也能顺利恢复当前进度，继续运行。

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