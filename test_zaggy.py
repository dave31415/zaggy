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
        self.mock = make_l1tf_mock(do_plot=False)
        self.y = self.mock['y_with_seasonal']
        self.num = len(self.y)
        self.dates = date_range(2015, 1, 2029, 12)[0:self.num]
        self.assertEquals(len(self.y), len(self.dates))
        seas_func = lambda date: date.month-1
        self.seasonality_matrix = \
            get_seasonality_matrix(self.dates,
                                   seasonality_function=seas_func)

    def test_l1_fit_runs(self):
        index = np.arange(self.num)
        result = l1_fit(index, self.y,
                        seasonality_matrix=self.seasonality_matrix)
        self.assertEquals(len(result['model']), self.num)

    def test_l1_fit_runs_correctly(self):
        # how low can we shrink this tolerance and still pass?
        tol = 0.03
        index = np.arange(self.num)
        result = l1_fit(index, self.y,
                        seasonality_matrix=self.seasonality_matrix)
        model = result['model']
        self.assertEquals(len(model), self.num)
        for x_value, y_value, model_value in zip(index, self.y, model):
            diff = model_value - y_value
            print x_value, y_value, model_value, diff
            self.assertLess(abs(diff), tol)
        assert True



if __name__ == "__main__":
    unittest.main()