from collections import Counter
from matrix_utils import zero_spmatrix


def get_compression_dict(indices):
    """
    Used to map a set of indices into a new index with no gaps
    and ignores indices not repeated.
    Used to remove unconstrainable indices and allow using
    matrix math
    :param indices: a list of indices, some of which are repeated
    :return: a dictionary that compresses them into another index
             with no gaps and which ignores indices in the orginal
             list that occurs only once
    """
    count = Counter()
    for index in indices:
        count[index] += 1
    constrained_indices = sorted([i[0] for i in count.items() if i[1] > 1])
    compression_dict = {i: num for num, i in enumerate(constrained_indices)}
    return compression_dict


def get_seasonality_matrix(dates, seasonality_function):
    """
    Create a sparse matrix mapping one index of seasonality variable
    to each data-point
    :param dates: iterable of datetime or date objects
    :param seasonality_function: a function or lambda taking
    a datetime or date object to a seasonality index, for example
    lambda date: date.weekday() or
    lambda date: date.month
    :return: spmatrix (cvxopt)
    """
    indices = [seasonality_function(date) for date in dates]
    compression_dict = get_compression_dict(indices)

    seasonality_matrix = \
        get_seasonality_matrix_compressed(dates,
                                          seasonality_function,
                                          compression_dict)
    return seasonality_matrix, compression_dict


def get_seasonality_matrix_compressed(dates, seasonality_function, compression_dict):
    """
    Create a sparse matrix mapping one index of seasonality variable
    to each data-point
    :param dates: iterable of datetime or date objects
    :param seasonality_function: a function or lambda taking
    :param compression_dict: a dictionary compressing the indices
    a datetime or date object to a seasonality index, for example
    lambda date: date.weekday() or
    lambda date: date.month
    :return: spmatrix (cvxopt)
    """

    seasonality_indices = [compression_dict[seasonality_function(date)]
                           for date in dates]
    assert min(seasonality_indices) >= 0
    seasonality_index_max = max(seasonality_indices)

    seasonality_matrix = zero_spmatrix(len(dates), seasonality_index_max+1)

    for row, column in enumerate(seasonality_indices):
        seasonality_matrix[row, column] = 1.0



    return seasonality_matrix

