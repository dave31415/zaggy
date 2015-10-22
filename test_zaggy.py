import unittest
from unittest import TestCase
from mocks import make_l1tf_mock
from seasonality import get_seasonality_matrix
from test_seasonality import date_range
from zaggy import l1_fit
import numpy as np


class TestZaggy(TestCase):
    """
    Test the zaggy time series fitting with some seasonality
    """

    def setUp(self):
        self.mock = make_l1tf_mock()
        self.y = self.mock['y_with_seasonal']
        self.num = len(self.y)
        self.dates = date_range(2015, 1, 2029, 12)[0:self.num]
        self.assertEquals(len(self.y), len(self.dates))
        seas_func = lambda date: date.month-1
        self.seasonality_matrix = get_seasonality_matrix(self.dates,
                                        seasonality_function=seas_func)

    def test_zaggy(self):
        index = np.arange(self.num)
        result = l1_fit(index, self.y,
                        seasonality_matrix=self.seasonality_matrix)
        self.assertEquals(len(result['model']), self.num)




if __name__ == "__main__":
    unittest.main()