import time
from datetime import datetime, timezone, timedelta

print(time.time())
print(datetime.utcnow().timestamp())  # weird
print(datetime.now(timezone.utc).timestamp())
print(datetime.now(timezone(timedelta(hours=2))).timestamp())

now = datetime.now()
print(now)

timestamp = 1257227555
dt_object = datetime.fromtimestamp(timestamp)
print("dt_object =", dt_object)
strftime = dt_object.strftime('%Y-%m-%d')
print(strftime)

date_begin_str = '2009-07-15'
date_begin = datetime.strptime(date_begin_str, '%Y-%m-%d')
print(date_begin.year, date_begin.month, date_begin.day)
