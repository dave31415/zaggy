import numpy as np
import date_scaling as ds
import datetime


def make_dates(num, time_unit=(1, 'day'), start_date=None):
    """
    Return an array of dates equally spaced in time
    If you want first of every month (not equally spaced in time)
    use datescaling.date_range instead
    :param num: number of dates requested
    :param time_unit: example (1, 'day') which is default
    :param start_date: the first datetime
    :return:
    """
    assert num > 0
    if start_date is None:
        start_date = datetime.datetime(2015, 1, 1)
    increment_seconds = time_unit[0]*ds.seconds_in_time_unit(time_unit[1])
    delta = datetime.timedelta(seconds=increment_seconds)

    t = [start_date]
    for i in xrange(num-1):
        t.append(t[-1] + delta)

    return np.array(t)


def make_random(num, seed=None):
    """
    Make a random-walk time-series pattern
    :param num: number of elements
    :param seed: random seed for repeatability
                 default None
    :return:
    """
    np.random.seed(seed)
    y = np.random.randn(num)
    # return the cumulative sum
    return np.cumsum(y)


def make_random_ts(num, seed=None, time_unit=(1, 'day')):
    """
    Make a random time series, both dates and y-value
    :param num: number of elements
    :param seed: random seed for repeatability
                 default None
    :param time_unit: example (1, 'day') which is default
    :return:
    """
    t = make_dates(num, time_unit)
    y = make_random(num, seed=seed)
    return t, y




