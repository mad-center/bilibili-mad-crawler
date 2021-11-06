import json
from pprint import pprint

from datetime import datetime
import time
import pymongo

from pymongo import UpdateOne

# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb://127.0.0.1:27017/test"
# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)


def test_connect():
    try:
        print(json.dumps(client.server_info()))
    except Exception as e:
        print("Unable to connect to the server.")


def test_get_db():
    try:
        print(client.test)
        # print(client['test'])
    # Database(MongoClient(host=['127.0.0.1:27017'], document_class=dict, tz_aware=False, connect=True,
    # serverselectiontimeoutms=5000), 'test')
    except Exception as e:
        print(e)


def test_get_collection():
    try:
        print(client.test.user)
        # Collection(Database(MongoClient(host=['127.0.0.1:27017'], document_class=dict, tz_aware=False, connect=True,
        #                                 serverselectiontimeoutms=5000), 'test'), 'user')
    except Exception as e:
        print(e)


def test_insert_one():
    try:
        new_user = {'name': 'admin', 'age': 10}
        result = client.test.user.insert_one(new_user)
        print(result)
        # < pymongo.results.InsertOneResult object at 0x0000023D7FBF2688 >
        print(result.inserted_id)
        # 61821835a3bca8298c3f8f3e

    # think how to avoid duplicated commit

    except Exception as e:
        print(e)


def test_find_one():
    try:
        result = client.test.user.find_one()
        print(result)
        # {'_id': ObjectId('618203f9efabb8b96117781f'), 'name': 'alice', 'age': 12, 'hobby': 'sing song'}
    except Exception as e:
        print(e)


def test_find_by_name():
    try:
        find_one = client.test.user.find_one({'name': 'bob'})
        print(find_one)
    except Exception as e:
        print(e)


def test_insert_many():
    try:
        new_users = [
            {
                'name': 'foo',
                'age': 15
            },
            {
                'name': 'bar',
                'age': 16
            }
        ]
        inser_many = client.test.user.insert_many(new_users)
        print(inser_many.inserted_ids)
    except Exception as e:
        print(e)


def test_counting():
    try:
        count_documents = client.test.user.count_documents({})
        print(count_documents)
    except Exception as e:
        print(e)


def test_range_query():
    try:
        user_find = client.test.user.find({'age': {'$lt': 16}})
        print(user_find)
        for user in user_find:
            print(user)
    except Exception as e:
        print(e)


def test_create_indexing():
    try:
        db = client.test
        result = db.profiles.create_index([('user_id', pymongo.ASCENDING)], unique=True)
        print(result)
        print(sorted(list(db.profiles.index_information())))
        # user_id_1
        # ['_id_', 'user_id_1']
    except Exception as e:
        print(e)


def test_insert_duplicate_data():
    try:
        db = client.test
        user_profiles = [
            {'user_id': 211, 'name': 'Luke'},
            {'user_id': 212, 'name': 'Ziltoid'}]
        result = db.profiles.insert_many(user_profiles)
        print(result)

        new_profile = {'user_id': 213, 'name': 'Drew'}
        duplicate_profile = {'user_id': 212, 'name': 'Tommy'}
        result = db.profiles.insert_one(new_profile)  # This is fine.
        print(result)
        result = db.profiles.insert_one(duplicate_profile)
        print(result)
        # E11000 duplicate key error collection: test.profiles index: user_id_1 dup key: { user_id: 212 }

    except Exception as e:
        print(e)


def test_bulk_write():
    try:
        operations = [
            UpdateOne({"vid": 1}, {'$set': {'vid': 1, 'desc': 'text 1'}}, upsert=True),
            UpdateOne({"vid": 2}, {'$set': {'vid': 2, 'desc': 'text 2'}}, upsert=True),
            UpdateOne({"vid": 3}, {'$set': {'vid': 3, 'desc': 'text 3'}}, upsert=True)
        ]
        collection = client.test.ids
        result = collection.bulk_write(operations)
        print(result)
        print('insert: {0}, delete: {1}, modify: {2}'.format(result.inserted_count,
                                                             result.deleted_count,
                                                             result.modified_count))
    except Exception as e:
        print(e)


def test_bulk_next_update():
    try:
        operations = [
            UpdateOne({"vid": 2}, {'$set': {'vid': 2, 'desc': 'text2 updated'}}, upsert=True),
            UpdateOne({"vid": 3}, {'$set': {'vid': 3, 'desc': 'text3 updated'}}, upsert=True),
            UpdateOne({"vid": 4}, {'$set': {'vid': 4, 'desc': 'text 4'}}, upsert=True),
            UpdateOne({"vid": 5}, {'$set': {'vid': 5, 'desc': 'text 5'}}, upsert=True)
        ]
        collection = client.test.ids
        result = collection.bulk_write(operations)
        print(result)
        print('insert: {0}, delete: {1}, modify: {2}'.format(result.inserted_count,
                                                             result.deleted_count,
                                                             result.modified_count))
    except Exception as e:
        print(e)


def test_get_mad_crawler_page():
    db = client['test']
    collection = db['mad_crawler_page']

    try:
        doc = collection.find_one()
        if doc:
            next_page = doc['page']
            return next_page
        else:
            return 1
    except Exception as e:
        print(e)
        return None


def test_init_mad_crawler_page():
    db = client['test']
    collection = db['mad_crawler_page']
    doc = {
        'page': 1,
        'last_update': datetime.now()
    }
    res = collection.insert_one(doc)
    pprint(res)


def test_update_mad_crawler_page():
    db = client['test']
    collection = db['mad_crawler_page']
    try:
        # find_one_and_update() Returns ``None`` if no document matches the filter.
        res = collection.find_one_and_update(
            {},
            {
                '$inc': {'page': 1},
                '$set': {'last_update': datetime.now()}
            },
            upsert=True
        )

        return res
    except Exception as e:
        pprint('ERROR: update page failed', e)
        return None

if __name__ == '__main__':
    test_update_mad_crawler_next_page()
