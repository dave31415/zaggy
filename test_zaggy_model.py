import unittest
from unittest import TestCase
from date_utils import date_range
from mocks import make_mock
from zaggy_model import ZaggyModel


class TestZaggyModel(TestCase):
    def setUp(self):
        mock = make_mock()
        self.y = mock['y_with_seasonal']
        num = len(self.y)
        self.dates = date_range(2015, 1, 2029, 12)[0: num]

    def test_zaggy_model_runs(self):
        self.model = ZaggyModel(self.dates, self.y)
        assert True

    def test_zaggy_model_fit_runs(self):
        self.model = ZaggyModel(self.dates, self.y)
        self.model.fit()
        assert True


if __name__ == "__main__":
    unittest.main()
