# chrome 请求分析

请求headers
```bash
accept: */*
accept-encoding: gzip, deflate, br
accept-language: en,zh-CN;q=0.9,zh;q=0.8
cookie: ...(省略)
referer: https://www.bilibili.com/v/douga/mad/
sec-ch-ua: "Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: script
sec-fetch-mode: no-cors
sec-fetch-site: same-site
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.46
```
- cookie：这里含有很多关于登录用户的真实信息。
- user-agent：用户代理。指代浏览器标识。
- sec-*： 只要包含前缀 Sec- 都属于应用程序禁止修改的HTTP消息头，用户代理保留全部对它们的控制权。

查询字符串
```
rid: 24
type: 0
pn: 1
ps: 20
jsonp: jsonp
callback: jsonCallback_bili_98964150959299252
```
- sonCallback_bili_98964150959299252 中的后缀数值是一个动态值。这个callback可以考虑不传。

响应headers
```bash
access-control-expose-headers: X-Cache-Webcdn
bili-status-code: 0
bili-trace-id: 505d3124cb618153
content-encoding: br
content-type: application/json; charset=utf-8
date: Tue, 02 Nov 2021 15:06:37 GMT
x-cache-webcdn: BYPASS from blzone01
```