# 记录爬虫进度——单一变量递增法

当需要爬虫的数据量很大时，短时间完成所有爬虫是不可能的。而且，由于爬虫涉及网络请求，程序处理， 数据库读写多方面的操作，很容易发生异常导致爬虫进度中断。

那么，就产生了以下问题：

- 如何记录爬虫当前已完成的进度？
- 如何从中断的位置开始，恢复爬虫？

爬虫本身应该是state-less的，也就是无状态。任何需要持久化的数据都应该放入数据库层。 保存爬虫进度，本质上是**保存当前情境的上下文**。

在当前分页爬取这个案例中，具体来说就是：

```
保存已成功爬取的page_number
```

例如page_number是50，代表1-50页已经被正常爬取，程序应当从51页开始继续运行。 page_number初始值是0。

这个方式，比较适合简单的单线程抓取模型。

## 实现

考虑到逻辑隔离，我决定拆分不同的爬取方式到独立的collection，来记录爬虫进度。

### 单线程-按页

在mongodb bilibili 数据库下新建一个集合 single_crawl_by_page。

|字段|类型|描述|
|---|---|---|
|_id|ObjectId|自带的ID标志|
|partition_name|String|分区名称|
|partition_code|String|分区代号|
|partition_id|Int32|分区rid|
|done_page|Int32|页码，表示已完成的页码进度|
|create_time|datetime|UTC 日期时间，表示爬虫开始时间|
|update_time|datetime|UTC 日期时间，表示最后一次成功爬虫的时间|

### 单线程-按日期

在mongodb bilibili 数据库下新建一个集合 single_crawl_by_date。

|字段|类型|描述|
|---|---|---|
|_id|ObjectId|自带的ID标志|
|partition_name|String|分区名称|
|partition_code|String|分区代号|
|partition_id|Int32|分区rid|
|done_date|String|日期，格式2007-09-07，表示已完成的日期进度|
|create_time|datetime|UTC 日期时间，表示爬虫开始时间|
|update_time|datetime|UTC 日期时间，表示最后一次成功爬虫的时间|
