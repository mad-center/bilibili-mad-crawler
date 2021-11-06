# 记录requests的异常

- 连接超时
- 等待超时

## ProxyError
```bash
HTTPSConnectionPool(host='api.bilibili.com', port=443):
Max retries exceeded with url: /x/web-interface/newlist?rid=24&type=0&pn=1&ps=20
(Caused by ProxyError('Cannot connect to proxy.', OSError(0, 'Error')))
```
本地代理错误。请设置本地电脑的代理，跳过api.bilibili.com这个host。也就是：
**不要对api.bilibili.com使用代理。**