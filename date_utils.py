import datetime


def date_range(start_year, start_month, end_year, end_month):
    """
    Create a list of consecutive date_times, one per month
    :param start_year: integer
    :param start_month: integer
    :param end_year: integer
    :param end_month: integer
    :return: array with all dates, month by month, in range (2014-12-1, 2015-1-1...)
    """

    result = [datetime.date(int(start_year), int(start_month), 1)]
    end = datetime.date(int(end_year), int(end_month), 1)

    while result[-1] < end:
        result.append((result[-1] + datetime.timedelta(days=32)).replace(day=1))

    return result