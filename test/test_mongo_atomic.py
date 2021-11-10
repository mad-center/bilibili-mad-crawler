from concurrent import futures
from datetime import datetime

import pymongo

conn_str = "mongodb://127.0.0.1:27017/test"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)


def mongo_increment():
    coll = client.test.atomic
    coll.find_one_and_update(
        {
            '_id': 1
        },
        {
            '$inc': {'count': 1}
        },
        upsert=True
    )


with futures.ThreadPoolExecutor(max_workers=3) as executor:
    tries = 500000

    time1 = datetime.now()
    res = [executor.submit(mongo_increment) for _ in range(tries)]
    futures.wait(res)
    time2 = datetime.now()
    print('time elapsed(s): ', (time2 - time1).seconds)

    for response in res:
        result = response.result()

    # mongo final is 500000, right
