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

year = 2020

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


def daily_average_number_of_publication():
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


def up_with_the_highest_number_of_publication():
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


def publication_with_the_highest_number_of(criterion='view'):
    project_more = {
        '$project': {
            'aid': '$aid',
            criterion: f'$stat.{criterion}',
            'pubdate_str': {
                '$toDate': {
                    '$multiply': ["$pubdate", 1000]
                }
            }
        }
    }
    sort_by_what = {
        '$sort': {
            criterion: -1
        }
    }
    limit = {
        '$limit': 20
    }
    pipeline = [
        project_more,
        match,
        sort_by_what,
        limit
    ]
    cursor = current_collection.aggregate(pipeline, **aggregation_params)
    results = list(cursor)
    return results


def copyright_total_count(copyright=1):
    project_more = {
        '$project': {
            'copyright': '$copyright',
            'pubdate_str': {
                '$toDate': {
                    '$multiply': ["$pubdate", 1000]
                }
            }
        }
    }
    group_by_month = {
        '$group': {
            '_id': '$copyright',
            '_count': {
                '$sum': 1
            }
        }
    }
    pipeline = [
        project_more,
        match,
        group_by_month,
    ]
    cursor = current_collection.aggregate(pipeline, **aggregation_params)
    results = list(cursor)

    dict = {}
    for idx, result in enumerate(results):
        dict[result['_id']] = result['_count']

    return dict.get(copyright, 0)


def cooperation_total_count():
    match_cooperation = {
        '$match': {
            # TODO not work
            'state': {
                '$eq': 0
            }
        }
    }
    count = {"$count": "count"}
    pipeline = [
        project,
        match,
        match_cooperation,
        count
    ]
    cursor = current_collection.aggregate(pipeline, **aggregation_params)
    results = list(cursor)
    return results


# print('year_total_count: ', year_total_count())
# print('daily_average_number_of_publication: ', daily_average_number_of_publication())
# print(every_month_publishing())

# print(publication_with_the_highest_number_of(criterion='view'))
# print(publication_with_the_highest_number_of(criterion='danmaku'))
# print(publication_with_the_highest_number_of(criterion='reply'))
# print(publication_with_the_highest_number_of(criterion='favorite'))
# print(publication_with_the_highest_number_of(criterion='coin'))
# print(publication_with_the_highest_number_of(criterion='share'))
# print(publication_with_the_highest_number_of(criterion='like'))

# copyright 1：原创 2：转载
# original_count = copyright_total_count(copyright=1)
# reproduce_count = copyright_total_count(copyright=2)
# total_count = year_total_count()
# print('(copyright=1): ', original_count)
# print('(copyright=2): ', reproduce_count)
# print('(copyright=1) percent: ', f'{original_count / total_count :.0%}')
# print('(copyright=2) percent: ', f'{reproduce_count / total_count:.0%}')

print(cooperation_total_count())
