import pandas as pd

date_range = [d.strftime('%Y-%m-%d') for d in pd.date_range('2009-09-01', '2009-12-07', freq='D')]
print(date_range)
