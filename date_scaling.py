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


def date_to_number(date):
    """
    Convert a datetime.datetime or datetime.date object to
    a number, seconds since Jan, 1, 1970
    :return:
    """
    if isinstance(date, datetime.date):
        #convert to datetime
        date = datetime.datetime(*(date.timetuple()[:6]))
    return (date - datetime.datetime(1970, 1, 1)).total_seconds()


def seconds_in_time_unit(unit):
    """
    Return the number of seconds in the given time unit
    :param unit: string: year, month, week, day, hour, minute, seconds
                 (or abbreviations min, sec)
    :return:
    """
    seconds_in_a_year = float(31557600)

    seconds = {'year': seconds_in_a_year,
               'month': seconds_in_a_year/12.0,
               'day': seconds_in_a_year/365.25,
               'hour': 3600.0,
               'minute': 60.0,
               'min': 3600.0,
               'second': 1.0,
               'sec': 1.0}

    # allow for plural,e.g. day or days treated the same
    # and case insensitivity

    unit = unit.lower()
    if unit[-1] == 's':
        unit = unit[:-1]

    return seconds[unit]


def scale_numbers(number, timescale):
    """
    :param number: a number
    :param timescale: a timescale tuple, e.g. (1,'day')
    :return:
    """
    timescale_number = float(timescale[0])
    timescale_unit = timescale[1]
    timescale_seconds = timescale_number*seconds_in_time_unit(timescale_unit)
    return number/timescale_seconds


def scale_date(date, timescale):
    """
    Convert date to a scaled number
    :param date: datetime.datetime or datetime.date object
    :param timescale: a tuple like (1,'day')
    :return: scaled date number
    """
    number = date_to_number(date)
    return scale_numbers(number, timescale)

