import time

import pymongo
import requests

from pymongo import UpdateOne

conn_str = "mongodb://127.0.0.1:27017/test"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client['test']
collection = db['mad']


def upsert_to_db(data):
    if data:
        print('count={0}, num={1}, size={2}, archives size={3}'
              .format(data['page']['count'], data['page']['num'], data['page']['size'], len(data["archives"])))

        print('Now inserting to db')

        mads = data['archives']
        operations = []
        for idx, mad in enumerate(mads):
            # mad = mads[idx]
            print(mad)
            filter = {'aid': mad['aid']}
            update = {'$set': mad}
            operations.append(UpdateOne(filter, update, upsert=True))

        print('operations=', operations)
        try:
            result = collection.bulk_write(operations)
            print(result)
            print('insert: {0}, delete: {1}, modify: {2}'.format(result.inserted_count,
                                                                 result.deleted_count,
                                                                 result.modified_count))
        except Exception as e:
            print(e)


def fetch_page(pn=1, ps=20):
    # url
    path = 'https://api.bilibili.com/x/web-interface/newlist'
    rid = 24
    type = 0
    pn = pn
    ps = ps
    url = f'{path}?rid={rid}&type={type}&pn={pn}&ps={ps}'
    print('url={0}'.format(url))

    try:
        r = requests.get(url)
        json = r.json()
        if json and json['code'] == 0:
            return json['data']
        else:
            print('response ok but no data')
            return None
    except Exception as e:
        # HTTPSConnectionPool(host='api.bilibili.com', port=443):
        # Max retries exceeded with url: /x/web-interface/newlist?rid=24&type=0&pn=1&ps=20
        # (Caused by ProxyError('Cannot connect to proxy.', OSError(0, 'Error')))
        print(e)
        return None


def crawl():
    for i in range(1, 2):
        data = fetch_page(pn=i)
        time.sleep(2)
        upsert_to_db(data)


if __name__ == '__main__':
    crawl()
