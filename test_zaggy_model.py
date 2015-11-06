import unittest
from unittest import TestCase
from date_scaling import date_range
from mocks import make_mock
from zaggy_model import ZaggyModel
from numpy import ndarray


class TestZaggyModel(TestCase):
    def setUp(self):
        mock = make_mock()
        self.y = mock['y']
        num = len(self.y)
        self.dates = date_range(2015, 1, 2029, 12)[0: num]

    def test_zaggy_model_runs(self):
        self.model = ZaggyModel(self.dates, self.y)
        assert True

    def test_zaggy_model_fit_runs(self):
        self.model = ZaggyModel(self.dates, self.y)
        self.assertIsNone(self.model.solution)
        self.model.fit()
        self.assertIsNotNone(self.model.solution)
        self.assertIsNotNone(self.model.slope)
        self.assertIsNotNone(self.model.offset)
        self.assertIsNotNone(self.model.seasonal)
        self.assertIsNotNone(self.model.interpolate)
        self.assertIsNotNone(self.model.extrapolate_without_seasonal)
        self.assertIsNotNone(self.model.seasonality_function)

    def test_zaggy_predict_on_fitted_points(self):
        self.model = ZaggyModel(self.dates, self.y)
        self.model.fit()
        results = self.model.predict(self.dates)
        assert isinstance(results, ndarray)
        for expected, result in zip(self.model.solution['model'], results):
            self.assertEquals(expected, result)

    def test_zaggy_predict_is_zero_on_dates_before_first_data_point(self):
        self.model = ZaggyModel(self.dates, self.y)
        self.model.fit()

        old_dates = date_range(2013, 1, 2014, 12)
        results = self.model.predict(old_dates)
        for expected, result in zip(self.model.solution['model'], results):
            self.assertEquals(result, 0.0)




if __name__ == "__main__":
    unittest.main()
