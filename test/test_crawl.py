import math
import time
from concurrent import futures
from datetime import datetime, date

import pymongo
import requests
from fake_useragent import UserAgent
from pymongo import UpdateOne

import crawl_config as config

# url config
primary_partition_name = 'N/A'
primary_partition_code = config.primary_partition_code
primary_partition_tid = 'N/A'

subpartition_name = config.subpartition_name
subpartition_code = config.subpartition_code
subpartition_tid = config.subpartition_tid

path = 'https://api.bilibili.com/x/web-interface/newlist'
type = 0
rid = subpartition_tid
ps = 50

# requests config
referer = f'https://www.bilibili.com/v/{primary_partition_code}/{subpartition_code}'

# db config
db_name = config.db_name if config.db_name else 'bilibili'

conn_str = f"{config.mongodb_url}{db_name}"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

db = client[db_name]
current_collection = db[subpartition_code]
crawl_progress_collection = db[config.crawl_progress_collection_name]


def total_video_count():
    url = page_url(path, rid, type, pn=1, ps=50)
    data = fetch_page(url)
    if data:
        return int(data['page']['count'])
    else:
        return None


def random_useragent():
    ua = UserAgent()
    return ua.random


def request_headers(referer='', random_ua=True):
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
        'referer': referer,
        'user-agent': random_useragent() if random_ua else ua
    }
    return headers


def insert_archives(data, log=False):
    if data and len(data['archives']) > 0:
        archives = data['archives']
        try:
            result = current_collection.insert_many(archives)
            if log:
                print('insert: {0}, delete: {1}, modify: {2}'.format(result.inserted_count,
                                                                     result.deleted_count,
                                                                     result.modified_count))
            return True
        except Exception as e:
            print('ERROR: bulk_write ', e)
    else:
        print('insert_archives: data is None.')

    return False


def upsert_archives(data, log=False):
    if data and len(data['archives']) > 0:
        archives = data['archives']
        operations = []

        for idx, archive in enumerate(archives):
            filter = {'aid': archive['aid']}
            update = {'$set': archive}
            operations.append(UpdateOne(filter, update, upsert=True))

        try:
            result = current_collection.bulk_write(operations)
            if log:
                print('insert: {0}, delete: {1}, modify: {2}'.format(result.inserted_count,
                                                                     result.deleted_count,
                                                                     result.modified_count))
            return True
        except Exception as e:
            print('ERROR: bulk_write ', e)

    else:
        print('upsert_archives() data is None.')

    return False


def fetch_page(url, retry_max=3, timeout=10):
    retry_count = 0
    retry_max = retry_max

    while retry_count <= retry_max:
        try:
            headers = request_headers(referer)
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


def page_url(path, rid, type, pn=1, ps=50):
    pn = pn
    ps = ps
    url = f'{path}?rid={rid}&type={type}&pn={pn}&ps={ps}'
    return url


def crawl_progress(type='page'):
    try:
        filter = {
            'partition_id': rid
        }
        doc = crawl_progress_collection.find_one(filter=filter)
        if doc:
            return doc['done_page']
        else:
            # 0 is initial value for done_page field
            return 0
    except Exception as e:
        print('ERROR: get next_page failed. MUST stop.')
        return None


def upsert_crawl_progress(type='page'):
    try:
        # find_one_and_update() Returns ``None`` if no document matches the filter.
        res = crawl_progress_collection.find_one_and_update(
            {
                'partition_id': rid
            },
            {
                '$setOnInsert': {
                    'partition_id': rid,
                    'create_time': datetime.now(),
                    'partition_name': subpartition_name,
                    'partition_code': subpartition_code
                },
                '$inc': {'done_page': 1},
                '$set': {'update_time': datetime.now()}
            },
            upsert=True
        )
        return True
    except Exception as e:
        print('ERROR: update page failed', e)

    return False


def earliest_video_date():
    total_count = total_video_count()
    page_count = math.ceil(total_count / ps)
    last_url = page_url(path, rid, type, pn=page_count, ps=ps)

    data = fetch_page(last_url)
    if data and len(data['archives']) > 0:
        archives = data['archives']
        pubdate = archives[0]['pubdate']

        for idx, archive in enumerate(archives):
            pubdate_ = archive['pubdate']
            if pubdate_ < pubdate:
                pubdate = pubdate_

        date_begin_str = datetime.fromtimestamp(pubdate).strftime('%Y-%m-%d')
        date_begin = datetime.strptime(date_begin_str, '%Y-%m-%d')
        return date(date_begin.year, date_begin.month, date_begin.day)

    return None


def single_crawl_by_page_range(page_start, page_end, ps, patch=False):
    for i in range(page_start, page_end + 1):

        url = page_url(path, rid, type, pn=i, ps=ps)
        print('url=', url)

        data = fetch_page(url)
        should_break = False

        if data and (len(data['archives']) > 0):
            print('count={0}, num={1}, size={2}, archives len={3}'
                  .format(data['page']['count'], data['page']['num'], data['page']['size'], len(data["archives"])))

            # do better: the all below ops should be wrapped by transaction
            if not patch:
                db_result = upsert_archives(data) and upsert_crawl_progress()
                should_break = not db_result
            else:
                db_result = upsert_archives(data)
                should_break = not db_result
        else:
            should_break = True
            print('ERROR: fetch page failed or data[archives] is empty.')

        if should_break:
            print('break in crawler: db OPS error or no data. cur page={0}'.format(i))
            break

        print('DONE: crawl page {0} and update page to {0}'.format(i, i))

        time.sleep(2)


def single_crawl_by_page():
    done_page = crawl_progress()
    total_count = total_video_count()
    page_count = math.ceil(total_count / ps)
    print(f'Analyze: done_page={done_page}, page_count={page_count}, page_count={total_count}')

    if done_page >= page_count:
        return

    next_page = done_page + 1
    single_crawl_by_page_range(next_page, page_count, ps)

    print('stop crawler.')


def single_crawl_by_date_range():
    # todo
    print()


def single_crawl_by_date():
    # todo
    date_begin = earliest_video_date()
    print(date_begin)


def multi_crawl_by_page_init_progress(page_count):
    if page_count > 0:
        # _id	page	data_size	state	update_time
        documents = [{'page': i, 'data_size': 0, 'state': False, 'update_time': None} for i in range(1, page_count + 1)]
        try:
            result = crawl_progress_collection.insert_many(documents)
            result_index = crawl_progress_collection.create_index([('page', pymongo.ASCENDING)], unique=True)
            if len(result.inserted_ids) > 0 and result_index:
                print('SUCCESS: multi_crawl_by_page_init_progress')
                return True
        except Exception as e:
            # E11000 duplicate key error
            # print(e)
            pass

    return False


def multi_crawl_by_page_tag_progress(page_num, data_size):
    result = crawl_progress_collection.update_one(
        {'page': page_num},
        {
            '$set': {'state': True, 'update_time': datetime.now(), 'data_size': data_size}
        }
    )

    return result.modified_count == 1


def random_select_page_nums(size=8):
    pipeline = [
        {
            "$match": {
                "state": False
            }
        },
        {
            "$sample": {
                "size": size
            }
        }
    ]
    cursor = crawl_progress_collection.aggregate(pipeline)
    docs = list(cursor)
    if len(docs) > 0:
        page_nums = [doc['page'] for doc in docs]
        return page_nums
    else:
        return []


def request_task(page_num):
    """
    thread task wrapper.
    """
    url = page_url(path, rid, type, pn=page_num, ps=50)
    return fetch_page(url)


def multi_crawl_by_page_nums(page_nums):
    with futures.ThreadPoolExecutor(max_workers=4, thread_name_prefix='crawler_thread_') as executor:
        tasks = [executor.submit(request_task, page_num) for i, page_num in enumerate(page_nums)]
        sets = futures.wait(tasks, timeout=10, return_when=futures.ALL_COMPLETED)

        for idx, task in enumerate(tasks):
            data = task.result()
            if data and len(data['archives']) > 0:
                # do better： multi thread mongo CRUD operations
                upsert_archives_feedback = insert_archives(data)
                if upsert_archives_feedback:
                    # print(f'UPDATE: crawl progress with page num - {page_nums[idx]}')
                    multi_crawl_by_page_tag_progress(page_num=page_nums[idx], data_size=len(data['archives']))
                else:
                    print('WARN: upsert archives succeed but update crawl progress failed ====> FAIL')
            else:
                # ignore this task no matter what happens
                print(f'WARN: ignore task with page number - {page_nums[idx]}')


def multi_crawl_by_page():
    total_count = total_video_count()
    page_count = math.ceil(total_count / ps)
    print(f'STATS: page_count={page_count}, total_count={total_count}')
    print('=' * 50)

    # init progress
    # SYNC
    init_progress = multi_crawl_by_page_init_progress(page_count=page_count)

    # get batch random page numbers from db
    page_nums_detect = random_select_page_nums(size=8)
    if len(page_nums_detect) == 0:
        print('FINISH:　No task in crawl progress.')
        return

    while True:
        page_nums = random_select_page_nums(size=8)
        print('SUCCESS: random select page nums', page_nums)

        # Note: `page_urls` and `tasks` below are parallel array. They have corresponding relation.
        multi_crawl_by_page_nums(page_nums)

        print('SUCCESS: multi_crawl_by_page_nums', page_nums)

        time.sleep(2)

        page_nums = random_select_page_nums(size=8)

        if len(page_nums) == 0:
            print('FINISH:　No task in crawl progress.')
            break


if __name__ == '__main__':
    # print(current_collection.count_documents({}))
    multi_crawl_by_page()
