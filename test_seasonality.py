import unittest
from unittest import TestCase
from seasonality import get_seasonality_matrix
import datetime


def date_range(start_year, start_month, end_year, end_month):
    """
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


class TestGetSeasonalityMatrix(TestCase):
    """
        Test get_seasonality_matrix with a few different
        choices of seasonality functions and date types/ranges
    """

    def test_get_seasonality_matrix_month(self):
        """
        Test that seasonality matrix works with month
        :return: None
        """
        dates = date_range(2013, 1, 2015, 8)
        #This maps Jan -> 0, Dec -> 11 etc
        seasonality_function = lambda date: date.month-1
        matrix = get_seasonality_matrix(dates, seasonality_function)
        n_dates = len(dates)
        n_months = 12
        self.assertEquals(matrix.size, (n_dates, n_months))
        # the first one which is Jan should be 1 for month index 0 and
        # 0 for every other month index
        self.assertEquals(matrix[0, 0], 1)
        for month_num in xrange(n_months):
            self.assertEquals(matrix[0, month_num], int(month_num == 0))
        # Test that the whole matrix is as expected
        for index in xrange(n_dates):
            for month_num in xrange(n_months):
                month_num_from_index = index % 12
                self.assertEquals(matrix[index, month_num],
                                  int(month_num == month_num_from_index))

    def test_get_seasonality_matrix_year(self):
        """
        Test that seasonality matrix works with year
        :return: None
        """
        dates = date_range(2013, 1, 2015, 8)
        #This maps 2013->0, 2014->1, 2015->2
        seasonality_function = lambda date: date.year-2013
        matrix = get_seasonality_matrix(dates, seasonality_function)
        n_dates = len(dates)
        n_years = 3
        self.assertEquals(matrix.size, (n_dates, n_years))
        # Test that the whole matrix is as expected
        for index in xrange(n_dates):
            for year_num in xrange(n_years):
                #integer division
                year_num_from_index = index / 12
                self.assertEquals(matrix[index, year_num],
                                  int(year_num == year_num_from_index))


if __name__ == "__main__":
    unittest.main()