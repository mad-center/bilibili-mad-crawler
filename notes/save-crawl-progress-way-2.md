# 记录爬虫进度——初始化-标记法

## 核心思路

- 初始化进度数据库。例如，已知需要爬取16000页。那么先创建一个表，定义其中一个列page，值分别从1递增到16000。批量写入数据库。 这样就得到了16000行记录，用来标志爬取进度。
- 在这个表，定义另外一个列state，类型为bool，值为true或者false。用来标志该页码爬取是否完成，该页爬虫完成就设置true。
- 不管爬虫程序如何设计，都根据state不为true的记录来获取任务。

## 适用场景

- 这个标记方法专门为多线程爬虫设计，单线程不需要这个方式。因为单线程同时只能更新一行记录，还不如退化为单一变量递增法。

## 实现

在mongodb bilibili 数据库下新建一个集合 multi_crawl_{name}_by_init_tag。name为需要爬取的分区名字或者代号。

### 表设计1

初始化

|_id|page|data_size|state|update_time|
|---|---|---|---|---|
|-| 1| |false| |
|-| 2| |false| |
|-| 3| |false| |
|- | ...| |false| |
|- | 15999| |false| |
|- | 16000| |false| |

> page 字段必须设置unique index。

中间状态示例: 线程随机获取记录行并更新

|_id|page|data_size|state|update_time|
|---|---|---|---|---|
|-| 1| |false| |
|-| 2| 50 |true| -|
|-| 3| |false| |
|- | ...|50 |true|- |
|- | 15999| |false| |
|- | 16000|34|true| -|

### 表设计2

初始化

|_id|date|data_size_array|state|update_time|
|---|---|---|---|---|
|-| 2009-07-15| |false| |
|-| 2009-07-16| |false| |
|-| 2009-07-17| |false| |
|- | ...| |false| |
|- | 2021-11-07| |false| |
|- | 2021-11-08| |false| |

> date 字段必须设置unique index。

中间状态

|_id|date|data_size_array|state|update_time|
|---|---|---|---|---|
|-| 2009-07-15|[1] |true|- |
|-| 2009-07-16|[50,39] |true| -|
|-| 2009-07-17| |false| |
|- | ...| |false| |
|- | 2021-11-07|[50,50,45] |true|- |
|- | 2021-11-08| |false| |

data_size_array是array类型，每个值分别表示特定页的稿件数。