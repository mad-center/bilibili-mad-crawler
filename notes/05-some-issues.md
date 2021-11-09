# some issues

## 爬虫进度-初始-标记法

![](./assets/multi_crawl_finish_by_init_tag_1.png)

## find duplicate aid

``` json
[
  {
    $group: {
      _id: "$aid",
      "dups": {
        "$push": "$_id"
      },
      count: {
        $sum: 1
      }
    }
  },
  {
    $match: {
      count: {
        $gt: 1
      }
    }
  }
]
```

![](./assets/duplicate_aid.png)

![](./assets/duplicate_documents.png)