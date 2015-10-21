from collections import Counter
from matrix_utils import zero_spmatrix


def get_seasonality_matrix(dates, seasonality_function):
    """
    Create a sparse matrix mapping one index of seasonality variable
    to each datapoint
    :param dates: iterable of datetime or date objects
    :param seasonality_function: a function or lambda taking
    a datetime or date object to a seasonality index, for example
    lambda date: date.weekday() or
    lambda date: date.month
    :return: spmatrix (cvxopt)
    """

    seasonality_indices = [seasonality_function(date) for date in dates]
    assert min(seasonality_indices) >= 0
    seasonality_index_max = max(seasonality_indices)

    seasonality_matrix = zero_spmatrix(len(dates), seasonality_index_max+1)

    for row, column in enumerate(seasonality_indices):
        seasonality_matrix[row, column] = 1.0

    if False:
        # do these unconstrained indices matter?
        # maybe not, ignore for now

        count = Counter()
        warnings = []
        unconstrained_indices = []
        for seasonality_index in seasonality_indices:
            count[seasonality_index] += 1
        for seasonality_index in xrange(seasonality_index_max):
            index_count = count[seasonality_index]
            if index_count < 2:
                warning = "Seasonality index: %s is present only %s times, " \
                          "not enough to be constrained" % (seasonality_index, index_count)
                warnings.append(warning)
                unconstrained_indices.append(seasonality_index)

    return seasonality_matrix

