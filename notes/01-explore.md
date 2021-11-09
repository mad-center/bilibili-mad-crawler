# Bilibili MAD区视频BGM探索

Bilibili MAD分区链接为： https://www.bilibili.com/v/douga/mad

## 初步尝试

- 请求网址: https://api.bilibili.com/x/web-interface/newlist?rid=24&type=0&pn=1&ps=20
- 请求方法: GET

响应数据示例：

```
{
    "code": 0,
    "message": "0",
    "ttl": 1,
    "data": {
        "archives": [
            ...//这里省略
        ],
        "page": {
            "count": 826846,
            "num": 1,
            "size": 20
        }
    }
}
```

注意到这里page对象：

- count，表示当前MAD分区一共含有826846个稿件。这个值随着时间推移是非常容易变化，逐步递增。 这里先将count随时间推移增长的问题搁置延迟，后续再考虑。
- num，表示当前是第1页。
- size，表示当前页面容量，一个页面最多含有20个稿件。（因为最后一页可能不会满20个。）这个值最高目前为50。

archives是一个数组，里面含有20个对象，每个对象表示对应稿件信息。下面选取其中一个对象archive进行分析：

```json
{
  "aid": 933974920,
  "videos": 1,
  "tid": 24,
  "tname": "MAD·AMV",
  "copyright": 1,
  "pic": "http://i1.hdslb.com/bfs/archive/7272ded00eca85e427dcb16bb1f9bf968c1907a5.jpg",
  "title": "【境界的彼方】前辈，能摸摸我的头吗",
  "pubdate": 1635826434,
  "ctime": 1635826434,
  "desc": "BGM：パズル---ENE",
  "state": 1,
  "duration": 267,
  "rights": {
    "bp": 0,
    "elec": 0,
    "download": 0,
    "movie": 0,
    "pay": 0,
    "hd5": 0,
    "no_reprint": 1,
    "autoplay": 1,
    "ugc_pay": 0,
    "is_cooperation": 0,
    "ugc_pay_preview": 0,
    "no_background": 0
  },
  "owner": {
    "mid": 140397571,
    "name": "御子香Yoyo",
    "face": "http://i1.hdslb.com/bfs/face/89e3231ca94bbf0924ce52b9a8657616fca11463.jpg"
  },
  "stat": {
    "aid": 933974920,
    "view": 1,
    "danmaku": 0,
    "reply": 0,
    "favorite": 0,
    "coin": 0,
    "share": 0,
    "now_rank": 0,
    "his_rank": 0,
    "like": 0,
    "dislike": 0
  },
  "dynamic": "",
  "cid": 434963002,
  "dimension": {
    "width": 1920,
    "height": 1080,
    "rotate": 0
  },
  "short_link": "https://b23.tv/BV1eT4y1d7mA",
  "short_link_v2": "https://b23.tv/BV1eT4y1d7mA",
  "first_frame": "http://i2.hdslb.com/bfs/storyff/n211102a2mx73axrgfvp24pav18r39ik_firsti.jpg",
  "bvid": "BV1eT4y1d7mA",
  "season_type": 0,
  "is_ogv": false,
  "ogv_info": null,
  "rcmd_reason": ""
}
```

可以见到这是一个含有很多字段的复杂对象，为了尽可能理解其中每个字段的含义。可以参考开源项目的
[这个页面](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/video/info.md) 。

## 技术决策

- 这样一个深层次嵌套的对象格式，在数据库保存方面，应该优先考虑document类型数据，例如mongodb。而不是关系型数据库，例如MySQL。
    - 为什么选择非关系型数据库？如果选择关系型，后续数据清洗（可能你需要数据清洗）之后，又需要重建一次数据表模式来保存。
      而对于document类型，取出数据，修改数据得到新对象，可以直接写到新的数据表。没有关系型数据库那种强范式约束。
- 在数据保存方面可以直接将整个响应原封不动地保存进数据。先不考虑数据清洗，即使数据中有很多数据我们并不关心。
    - 为什么不在爬虫的时候，同时将爬取的数据结果直接清洗放入数据库？一步到位不是更好吗？~~类似于为什么不在一个函数中做10件事情呢？~~
      主要还是关注点分离。爬虫的时候，只需要关注原始数据的抓取，不要考虑后续的数据处理。不要越界责任。

也就是，将爬取的数据直接保存进mongodb的数据库对应的表。

## 关心的字段

这里我只关心我感兴趣的字段。
> 为了减少数据保存的数据量以及关注点集中。对于关心的字段，我会直接使用markdown的强调语义将其标记为粗体。

- **aid**： 稿件avid。
- videos： 稿件分P总数，默认为1。
- tid：分区tid。这里是24。
- tname：分区名称。这里是MAD·AMV
- copyright: 视频类型。1：原创。2：转载。
- pic：稿件封面图片url。
- **title**：稿件标题。
- pubdate：稿件发布时间。时间戳数值。
- ctime：用户投稿时间。时间戳数值。
- **desc**：视频简介。字符串类型。这个是重要的关注字段。提取BGM的关键。
- **desc_v2**：新版视频简介。array类型。
    - **raw_text**: 简介内容。这个是重要的关注字段。提取BGM的关键。
    - type
    - biz_id
- ~~state：稿件状态。不关心这个字段。能搜索到的基本就是合格稿件。~~
- duration：稿件总时长(所有分P)。秒单位。
- ~~rights：视频属性标志。不关心这个字段。~~
- owner：up主。
    - mid：up主id
    - name：up名称
    - face: up头像
- stat
    - aid: 稿件aid
    - view: 播放数
    - danmaku: 弹幕数
    - reply: 评论数
    - favorite: 收藏数
    - coin: 投币数
    - share: 分享数
    - now_rank: 当前排名
    - his_rank: 历史最高排行
    - like: 获赞数
    - dislike: 点踩数。固定为0？
- dynamic: 视频同步发布的的动态的文字内容。
- cid: 视频1P cid。
- dimension: 视频1P分辨率。
- ...

