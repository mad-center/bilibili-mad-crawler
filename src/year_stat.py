import collections
import json
import os
from datetime import datetime
from pathlib import Path

import pymongo
from bson import json_util


class YearStat:
    def __init__(self, config, year):
        # db config
        self.db_name = config.db_name if config.db_name else 'bilibili'
        self.conn_str = f"{config.mongodb_url}{self.db_name}"
        self.client = pymongo.MongoClient(self.conn_str, serverSelectionTimeoutMS=5000)

        self.db = self.client[self.db_name]
        self.current_collection = self.db[config.subpartition_code]
        self.crawl_progress_collection = self.db[config.crawl_progress_collection_name]

        # year
        self.year = year

        # basic QL and aggregation params
        self.project = {
            '$project': {
                'pubdate_str': {
                    '$toDate': {
                        '$multiply': ["$pubdate", 1000]
                    }
                }
            }
        }
        self.match = {
            '$match': {
                'pubdate_str': {
                    '$gte': datetime.strptime(f'{self.year}-01-01', '%Y-%m-%d'),
                    '$lt': datetime.strptime(f'{self.year + 1}-01-01', '%Y-%m-%d'),
                }
            }
        }
        self.aggregation_params = {'allowDiskUse': True}

    @staticmethod
    def _days_of_year(year):
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

    @staticmethod
    def parse_json(data):
        return json.loads(json_util.dumps(data))

    def year_total_count(self, ):
        count = {"$count": "count"}
        pipeline = [
            self.project,
            self.match,
            count
        ]
        cursor = self.current_collection.aggregate(pipeline, **self.aggregation_params)
        return int(list(cursor)[0]['count'])

    def daily_average_number_of_publication(self, ):
        result = self.year_total_count() / self._days_of_year(2009)
        return round(result, 3)

    def every_month_publishing(self, ):
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
            self.project,
            self.match,
            project_month,
            group_by_month
        ]
        cursor = self.current_collection.aggregate(pipeline, **self.aggregation_params)
        results = list(cursor)

        # init dict
        dict = {}
        for idx in range(1, 12 + 1):
            dict[f'{self.year}-' + f'{idx:02}'] = 0

        #  assign
        for idx, result in enumerate(results):
            dict[result['_id']] = result['_count']

        #  convert dict to ordered dict
        ordered_dict = collections.OrderedDict(sorted(dict.items()))
        return ordered_dict

    def up_with_the_highest_number_of_publication(self, ):
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
        limit = {
            '$limit': 20
        }
        pipeline = [
            project_more,
            self.match,
            group_by_mid,
            sort_by_count,
            limit
        ]
        cursor = self.current_collection.aggregate(pipeline, **self.aggregation_params)
        results = list(cursor)
        return results

    def publication_with_the_highest_number_of(self, criterion='view'):
        project_for_match = {
            '$project': {
                'aid': '$aid',
                criterion: f'$stat.{criterion}',
                'bvid': '$bvid',
                'pubdate_str': {
                    '$toDate': {
                        '$multiply': ["$pubdate", 1000]
                    }
                }
            }
        }
        unset_fields = {
            '$unset': ['_id', 'pubdate_str']
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
            project_for_match,
            self.match,
            unset_fields,
            sort_by_what,
            limit
        ]
        cursor = self.current_collection.aggregate(pipeline, **self.aggregation_params)
        results = list(cursor)
        return results

    def copyright_total_count(self, copyright=1):
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
            self.match,
            group_by_month,
        ]
        cursor = self.current_collection.aggregate(pipeline, **self.aggregation_params)
        results = list(cursor)

        dict = {}
        for idx, result in enumerate(results):
            dict[result['_id']] = result['_count']

        return dict.get(copyright, 0)

    def cooperation_total_count(self):
        project_more = {
            '$project': {
                'is_cooperation': '$rights.is_cooperation',
                'pubdate_str': {
                    '$toDate': {
                        '$multiply': ["$pubdate", 1000]
                    }
                }
            }
        }
        match_cooperation = {
            '$match': {
                'is_cooperation': {
                    '$eq': 1
                }
            }
        }
        count = {"$count": "_count"}
        pipeline = [
            project_more,
            self.match,
            match_cooperation,
            count
        ]
        cursor = self.current_collection.aggregate(pipeline, **self.aggregation_params)
        results = list(cursor)
        return results[0]['_count'] if len(results) > 0 else 0

    def dump_to_file(self, data=None, filename='data.json'):
        if data is not None and filename:
            default_folder = f'../stats/{self.year}/'

            # make sure dir exists
            Path(default_folder).mkdir(parents=True, exist_ok=True)

            # check certain file  exists
            filename_ = f'{default_folder}{filename}'
            if not os.path.exists(filename_):
                with open(filename_, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

    def dump_all(self, ):
        total_count = self.year_total_count()
        self.dump_to_file(total_count, filename='year_total_count.json')

        daily_average_publication = self.daily_average_number_of_publication()
        self.dump_to_file(daily_average_publication, filename='daily_average_publication.json')

        month_publishing = self.every_month_publishing()
        self.dump_to_file(month_publishing, filename='month_publishing.json')

        stat_view = self.publication_with_the_highest_number_of(criterion='view')
        self.dump_to_file(self.parse_json(stat_view), filename='stat_view.json')

        stat_danmaku = self.publication_with_the_highest_number_of(criterion='danmaku')
        self.dump_to_file(self.parse_json(stat_danmaku), filename='stat_danmaku.json')

        stat_reply = self.publication_with_the_highest_number_of(criterion='reply')
        self.dump_to_file(self.parse_json(stat_reply), filename='stat_reply.json')

        stat_favorite = self.publication_with_the_highest_number_of(criterion='favorite')
        self.dump_to_file(self.parse_json(stat_favorite), filename='stat_favorite.json')

        stat_coin = self.publication_with_the_highest_number_of(criterion='coin')
        self.dump_to_file(self.parse_json(stat_coin), filename='stat_coin.json')

        stat_share = self.publication_with_the_highest_number_of(criterion='share')
        self.dump_to_file(self.parse_json(stat_share), filename='stat_share.json')

        stat_like = self.publication_with_the_highest_number_of(criterion='like')
        self.dump_to_file(self.parse_json(stat_like), filename='stat_like.json')

        # copyright 1：原创 2：转载
        original_count = self.copyright_total_count(copyright=1)
        reproduce_count = self.copyright_total_count(copyright=2)
        total_count = self.year_total_count()
        original_percent = f'{original_count / total_count :.0%}'
        reproduce_percent = f'{reproduce_count / total_count :.0%}'
        self.dump_to_file([original_count, original_percent], filename='original.json')
        self.dump_to_file([reproduce_count, reproduce_percent], filename='reproduce.json')

        cooperation_count = self.cooperation_total_count()
        self.dump_to_file(cooperation_count, filename='cooperation.json')
