import unittest
from unittest import TestCase
from seasonality import get_seasonality_matrix, get_compression_dict
from date_scaling import date_range


# TODO: these aren't really unit tests
# TODO: get_seasonality_matrix_compressed could be unit tested
# TODO: rather than testing the wrapper function which tests both
# TODO: things at once. But Ok for now.


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
        matrix, compression = get_seasonality_matrix(dates, seasonality_function)
        for key, val in compression.items():
            self.assertEquals(val, key)

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
        matrix, compression = get_seasonality_matrix(dates, seasonality_function)
        expected_compression = {0: 0, 1: 1, 2: 2}
        self.assertDictEqual(compression, expected_compression)
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

    def test_get_seasonality_matrix_year_with_gap(self):
        """
        Test that seasonality matrix works with year and a gap year
        :return: None
        """
        dates = [d for d in date_range(2013, 1, 2015, 8) if d.year != 2014]
        #This maps 2013->0, 2015->2
        seasonality_function = lambda date: date.year-2013
        matrix, compression = get_seasonality_matrix(dates, seasonality_function)
        expected_compression = {0: 0, 2: 1}
        self.assertDictEqual(compression, expected_compression)
        n_dates = len(dates)
        # now only 2 years
        n_years = 2
        self.assertEquals(matrix.size, (n_dates, n_years))
        # Test that the whole matrix is as expected
        for index in xrange(n_dates):
            for year_num in xrange(n_years):
                #integer division
                year_num_from_index = index / 12
                self.assertEquals(matrix[index, year_num],
                                  int(year_num == year_num_from_index))


class TestCompression(TestCase):
    """
    Test that the compression dictionary works on a few test cases
    """
    def test_compress1(self):
        indices = [19, 19, 0, 1, 2, 2, 3, 4, 4, 4, 9, 14, 14]
        compression_dict = get_compression_dict(indices)
        expected = {2: 0, 4: 1, 14: 2, 19: 3}
        self.assertDictEqual(compression_dict, expected)

    def test_compress2(self):
        indices = [99, 14, 14, 88, 3, 3, 3, 12, 12]
        compression_dict = get_compression_dict(indices)
        expected = {3: 0, 12: 1, 14: 2}
        self.assertDictEqual(compression_dict, expected)

    def test_compress_no_repeats(self):
        """
        No Repeated ones
        """
        indices = [66, 67, 888]
        compression_dict = get_compression_dict(indices)
        expected = {}
        self.assertDictEqual(compression_dict, expected)


if __name__ == "__main__":
    unittest.main()