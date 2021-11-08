import arrow


def days_of_year(year):
    """
    通过判断闰年，获取年份year的总天数

    :param year: 年份, int
    :return:days_sum, 年份year的总天数, 366 or 365
    """
    year = int(year)
    assert isinstance(year, int), "Please enter integer, for example: 2018"

    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_sum = 366
    else:
        days_sum = 365

    return days_sum


def day_list_of_year(year):
    """
    获取一年的所有日期

    :param year: 年份
    :return: list, 全部日期的列表
    """
    start_date = '%s-1-1' % year
    offset = 0
    date_list = []
    days_sum = days_of_year(int(year))
    while offset < days_sum:
        new_date = arrow.get(start_date).shift(days=offset).format("YYYY-MM-DD")
        date_list.append(new_date)
        offset += 1
    return date_list


if __name__ == '__main__':
    days_sum = days_of_year('2000')
    print(days_sum)

    # 获取一年的所有日期
    all_date_list = day_list_of_year(2000)
    print(all_date_list)
