# 处理requests的异常

- [ ] 超时主动放弃
- [x] 错误被动重试

## ProxyError

```bash
HTTPSConnectionPool(host='api.bilibili.com', port=443):
Max retries exceeded with url: /x/web-interface/newlist?rid=24&type=0&pn=1&ps=20
(Caused by ProxyError('Cannot connect to proxy.', OSError(0, 'Error')))
```

本地代理错误。请设置本地电脑的代理，跳过api.bilibili.com这个host。也就是：
**不要对api.bilibili.com使用代理。**

## TimeoutError

```bash
('Connection aborted.', TimeoutError(10060, '由于连接方在一段时间后没有正确答复或连接的主机没有反应，
连接尝试失败。', None, 10060, None))
```

解决方法：自定义重试机制。

## ConnectionResetError

```bash
ERROR: fetch_page ('Connection aborted.', ConnectionResetError(10054, 
 '远程主机强迫关闭了一个现有的连接。', None, 10054, None))
```

解决方法：自定义重试机制。

## 自定义重试机制

采取自定义的重试机制。下面是伪代码。

``` python
def fetch_page(url, retry_max=3):
    retry_count = 0
    retry_max = retry_max

    while retry_count <= retry_max:
        try:
            # make http request and return value
            return make_http_request()    
        except Exception as e:
            time.sleep(3)

            retry_count += 1
            print('fetch_page retry count: ', retry_count)

    return None
```

- 变量 retry_count 表示当前重试的次数。
- retry_max 为最大重试次数，提取为函数参数方便配置。
- 每次重试之前，稍微等待3秒，避免过于暴力的重试。

验证是否真实可用。图中在抓取8532页时发生报错，retry机制完美解决这个问题。程序没有中断。
![](./assets/valid-retry-http-works.png)