# MAD分区爬虫的统计

本文分析 multi_crawl_mad_by_init_tag 集合。

- 爬虫并行线程数 8(CPU逻辑处理器数量为8)
- 页数 16593
- MAD稿件数量 829621
- 爬虫开始时间：ISODate("2021-11-09T19:54:20.413+0000")
- 爬虫结束时间：ISODate("2021-11-09T21:43:30.030+0000")

```shell
db.getCollection(" multi_crawl_mad_by_init_tag").find({}).sort({ update_time: 1 }).limit(1)
db.getCollection(" multi_crawl_mad_by_init_tag").find({}).sort({ update_time: -1 }).limit(1)
```

- 爬虫持续时间：1h 50min左右。