import math
import time
import pymongo
import requests

from datetime import datetime
from fake_useragent import UserAgent
from pymongo import UpdateOne

conn_str = "mongodb://127.0.0.1:27017/test"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client['test']
mad_collection = db['mad']
page_collection = db['mad_crawler_page']


def mad_estimate_count():
    url = page_url(pn=1, ps=20)
    data = fetch_page(url)
    if data:
        return int(data['page']['count'])
    else:
        return None


def random_useragent():
    ua = UserAgent()
    return ua.random


def request_headers(random_ua=True):
    """
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
    """
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.46'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'referer': 'https://www.bilibili.com/v/douga/mad/',
        'user-agent': random_useragent() if random_ua else ua
    }
    return headers


def upsert_to_db(data):
    if data:
        mads = data['archives']
        if len(mads) > 0:
            operations = []
            for idx, mad in enumerate(mads):
                filter = {'aid': mad['aid']}
                update = {'$set': mad}
                operations.append(UpdateOne(filter, update, upsert=True))

            # print('operations=', operations)
            try:
                result = mad_collection.bulk_write(operations)

                print('insert: {0}, delete: {1}, modify: {2}'.format(result.inserted_count,
                                                                     result.deleted_count,
                                                                     result.modified_count))
                return True
            except Exception as e:
                print('ERROR: bulk_write ', e)
    else:
        print('upsert_to_db() data is None.')

    return False


def fetch_page(url, retry_max=3, timeout=10):
    retry_count = 0
    retry_max = retry_max

    while retry_count <= retry_max:
        try:
            headers = request_headers()
            r = requests.get(url, headers, timeout=timeout)
            json = r.json()
            if json and json['code'] == 0:
                return json['data']
            else:
                print('response ok but no data')
                return None
        except Exception as e:
            print('ERROR: fetch_page', e)
            time.sleep(3)

            retry_count += 1
            print('fetch_page retry count: ', retry_count)

    return None


def page_url(pn=1, ps=20):
    # url
    path = 'https://api.bilibili.com/x/web-interface/newlist'
    rid = 24
    type = 0
    pn = pn
    ps = ps
    url = f'{path}?rid={rid}&type={type}&pn={pn}&ps={ps}'
    return url


def mad_crawler_page():
    """
    情况分析：

    >>> 1. 数据库访问失败。返回None。
    >>> 2. 数据库访问成功，但是没有查询到doc，代表还没有初始化。直接返回0。
    >>> 3. 数据库访问成功，查询到doc，返回doc中的page字段。
    Returns
    -------

    """
    try:
        doc = page_collection.find_one()
        if doc:
            return doc['page']
        else:
            # 0 is initial page number
            return 0
    except Exception as e:
        print('ERROR: get next_page failed. MUST stop.')
        return None


def upsert_mad_crawler_page():
    try:
        # find_one_and_update() Returns ``None`` if no document matches the filter.
        res = page_collection.find_one_and_update(
            {},
            {
                '$setOnInsert': {'create_time': datetime.now()},
                '$inc': {'page': 1},
                '$set': {'last_update': datetime.now()}
            },
            upsert=True
        )

        # print(res)
        return True
    except Exception as e:
        print('ERROR: update page failed', e)

    return False


def crawl():
    ps = 50

    print('prepare begin' + ('=' * 50))
    # 已完成的爬取页码
    page = mad_crawler_page()
    # 当前稿件总数
    current_count = mad_estimate_count()

    page_count = math.ceil(current_count / ps)
    if page >= page_count:
        print('当前已经抵达爬虫页数的尽头', page, page_count, current_count)
        return

    # page_count = 3  # for local test
    print('page:{0}, page_count:{1}'.format(page, page_count))
    print('prepare end' + ('=' * 50))

    next_page = page + 1

    # extract this for logic to func
    crawl_by_range(next_page, page_count, ps)

    print('你又在爬虫啊，休息一下吧。')


def crawl_by_range(page_start, page_end, ps):
    for i in range(page_start, page_end + 1):
        print('begin crawl page ' + str(i) + ('=' * 50))
        url = page_url(pn=i, ps=ps)
        print('url=', url)

        data = fetch_page(url)
        should_break = False

        # Condition: len(data['archives']) > 0 保证有数据写入db的一致性。
        # 否则当出现页码尽头越界时，会造成page数字递增的错误，而此时没有mad数据写入。
        if data and (len(data['archives']) > 0):
            print('count={0}, num={1}, size={2}, archives len={3}'
                  .format(data['page']['count'], data['page']['num'], data['page']['size'], len(data["archives"])))

            # do better: the all below ops should be wrapped by transaction
            # upsert mad and save context(crawler progress): page
            # only upsert mad succeed can call upsert page function
            db_result = upsert_to_db(data) and upsert_mad_crawler_page()
            should_break = not db_result
        else:
            should_break = True
            print('ERROR: fetch page failed or data[archives] is empty.')

        print('end crawl page ' + str(i) + ('=' * 50))

        if should_break:
            print('break in crawler: db OPS error or no data. cur page={0}'.format(i))
            break

        print('DONE: crawl page {0} and update page to {0}'.format(i, i))
        # wait
        time.sleep(2)


if __name__ == '__main__':
    # crawl()
    crawl_by_range(1, 60, 50)
