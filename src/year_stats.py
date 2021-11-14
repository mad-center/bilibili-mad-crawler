import collections
from datetime import datetime

import pymongo

import crawl_config as config

# db config
db_name = config.db_name if config.db_name else 'bilibili'

conn_str = f"{config.mongodb_url}{db_name}"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

db = client[db_name]
current_collection = db[config.subpartition_code]
crawl_progress_collection = db[config.crawl_progress_collection_name]

year = 2009

# select
project = {
    '$project': {
        'pubdate_str': {
            '$toDate': {
                '$multiply': ["$pubdate", 1000]
            }
        }
    }
}

# where
match = {
    '$match': {
        'pubdate_str': {
            '$gte': datetime.strptime(f'{year}-01-01', '%Y-%m-%d'),
            '$lt': datetime.strptime(f'{year + 1}-01-01', '%Y-%m-%d'),
        }
    }
}

aggregation_params = {'allowDiskUse': True}


def __days_of_year(year):
    """
    通过判断是否闰年，获取年份year的总天数：366,或者365
    """
    year = int(year)
    assert isinstance(year, int), "Please enter integer, for example: 2018"

    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_sum = 366
    else:
        days_sum = 365

    return days_sum


def year_total_count():
    count = {"$count": "count"}
    pipeline = [
        project,
        match,
        count
    ]
    cursor = current_collection.aggregate(pipeline, **aggregation_params)
    return int(list(cursor)[0]['count'])


def daily_average_number_of_publishing():
    result = year_total_count() / __days_of_year(2009)
    return round(result, 3)


def every_month_publishing():
    project_month = {
        '$project': {
            'month_substr': {
                '$substr': ["$pubdate_str", 0, 7]
            },
        }
    }
    group_by_month = {
        '$group': {
            '_id': '$month_substr',
            '_count': {
                '$sum': 1
            }
        }
    }
    pipeline = [
        project,
        match,
        project_month,
        group_by_month
    ]
    cursor = current_collection.aggregate(pipeline, **aggregation_params)
    results = list(cursor)

    # init dict
    dict = {}
    for idx in range(1, 12 + 1):
        dict[f'{year}-' + f'{idx:02}'] = 0

    #  assign
    for idx, result in enumerate(results):
        dict[result['_id']] = result['_count']

    #  convert dict to ordered dict
    ordered_dict = collections.OrderedDict(sorted(dict.items()))
    return ordered_dict


def up_with_the_highest_number_of_publishing():
    project_more = {
        '$project': {
            'aid': '$aid',
            'mid': '$owner.mid',
            'pubdate_str': {
                '$toDate': {
                    '$multiply': ["$pubdate", 1000]
                }
            }
        }
    }
    group_by_mid = {
        '$group': {
            '_id': '$mid',
            '_count': {
                '$sum': 1
            }
        }
    }
    sort_by_count = {
        '$sort': {
            '_count': -1
        }
    }
    # limit result TOP 20 when length >=20
    limit = {
        '$limit': 20
    }
    pipeline = [
        project_more,
        match,
        group_by_mid,
        sort_by_count,
        limit
    ]
    cursor = current_collection.aggregate(pipeline, **aggregation_params)
    results = list(cursor)
    return results


# print('year_total_count: ', year_total_count())
# print('daily_average_number_of_publishing: ', daily_average_number_of_publishing())
# print(every_month_publishing())
print(up_with_the_highest_number_of_publishing())
