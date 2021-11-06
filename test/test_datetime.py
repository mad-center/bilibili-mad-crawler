import time
from datetime import datetime, timezone, timedelta

print(time.time())
print(datetime.utcnow().timestamp())  # weird
print(datetime.now(timezone.utc).timestamp())
print(datetime.now(timezone(timedelta(hours=2))).timestamp())


now = datetime.now()
print(now)