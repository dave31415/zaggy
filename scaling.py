import datetime


def date_to_number(date):
    """
    Convert a datetime.datetime or datetime.date object to
    a number, seconds since Jan, 1, 1970
    :return:
    """
    if isinstance(date, datetime.date):
        #convert to datetime
        date = datetime.datetime(*(date.timetuple()[:6]))
    return (date - datetime.datetime(1970,1,1)).total_seconds()


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

    return seconds[unit]


def scale_numbers(number, timescale):
    """
    :param number: a number
    :param timescale: a timescale tuple, e.g. (1,'day')
    :return:
    """
    timescale_number = timescale[0]
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

