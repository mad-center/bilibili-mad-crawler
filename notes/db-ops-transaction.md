# 数据库事务

## 自身实现
``` python
upsert_to_db(data) and upsert_mad_crawler_page()
```

情境描述：

- upsert_to_db(data) 将特定页码的mad信息写入db
- upsert_mad_crawler_page() 更新已完成的page信息

这两个数据库的写操作，应当满足数据库的事务，从而保证爬虫进度的一致性。

upsert_to_db() 和 upsert_mad_crawler_page() 返回值都是bool， 当且仅当操作成功返回True，其他情况一律返回False。

注意函数之间连接符号是and，然后列表分析：

|#|upsert_to_db|upsert_mad_crawler_page|结果|
|---|---|---|---|
|#1|True|True|两个都成功，完美。mad新增，page+1。可以进入下一页抓取。|
|#2|True|False|mad成功，page更新失败。mad新增，page没有+1。数据状态不一致。但是由于mad是upsert，下次插入数据不会产生重复。**停止下一页的抓取，重试当前page的抓取**。|
|#3|False|?|mad失败，page更新不会执行。mad和page表都不会更新。数据状态一致。**停止下一页的抓取，重试当前page的抓取**。|

总结：upsert_mad_crawler_page()这个method才是记录的关键。一旦 upsert_mad_crawler_page() 失败，就必须暂时停止下一页的抓取，并重试当前页的抓取。


## 依赖第三方库实现
类似于Spring Transaction库。设置@Transaction标记某个method。这个method就是事务方法。
这个method内一切DB操作要么全部成功，要么全部失败。