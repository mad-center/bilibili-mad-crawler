# bilibili mad crawler

> rename to bilibili-partition-crawler?

bilibili 分区视频的爬虫设计与实现。| A crawler design and implementation for bilibili partition video。

## 爬虫

- [x] 《论爬虫演员的自我修养》
- [x] 爬虫时间成本分析
- [x] bilibili MAD api分析：分页搜索和热度搜索
- [x] chrome 请求分析
- [x] 强悍的恢复能力：爬虫进度上下文的保存，随时中断和恢复
- [x] 数据库事务分析，
  - [x] 鸵鸟算法：忽略重复插入，不进行rollback
  - [ ] 事务：mongodb 需要开启replica set才能支持。
- [x] 多线程并行请求的分析
    - [x] 使用初始化-标记法。
- [x] HTTP请求异常（超时，或者错误）的重试机制
- [ ] TCP 连接池 by request.Session()
- [x] 衍生教程，讲述爬虫的设计和原理分析(notes/)
- [x] 爬虫机制
    - [x] 单线程-按页（仅供学习参考，爬取效率很低）
    - [ ] ~~单线程-按日期~~（不会被实现）
    - [x] 多线程-按页
    - [ ] 多线程-按日期
  
## 统计

- [x] 年度MAD总投稿量 => number
- [x] 年度MAD日均投稿数 => number
- [x] 年度每个月的MAD投稿数量 => result{}
- [x] 年度MAD投稿数最高的up TOP 20 => result[]
- [x] 年度MAD稿件播放量TOP 20 => result[]
- [x] 年度MAD稿件弹幕数TOP 20 => result[]
- [x] 年度MAD稿件评论数TOP 20 => result[]
- [x] 年度MAD稿件收藏数TOP 20 => result[]
- [x] 年度MAD稿件硬币数TOP 20 => result[]
- [x] 年度MAD稿件分享数TOP 20 => result[]
- [x] 年度MAD稿件点赞数TOP 20 => result[]
- [x] 年度MAD原创投稿数/占比 => number,number
- [x] 年度MAD转载投稿数/占比 => number,number
- [x] 年度MAD联合投稿数 => number
- [ ] 年度MAD投稿最具潜力的新up TOP 20: result[]