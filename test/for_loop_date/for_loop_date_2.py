from datetime import date, timedelta

day_begin = date(2009, 1, 1)  # start date
day_end = date(2009, 12, 31)  # end date
day_delta = day_end - day_begin  # timedelta

day_list = [day_begin + timedelta(i) for i in range(day_delta.days + 1)]
print(len(day_list))
