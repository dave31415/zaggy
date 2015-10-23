import unittest
from unittest import TestCase
import date_scaling as ds
import datetime


class TestDateScaling(TestCase):
    def test_date_range(self):
        expected = [datetime.date(2015, 1, 1), datetime.date(2015, 2, 1),
                    datetime.date(2015, 3, 1), datetime.date(2015, 4, 1),
                    datetime.date(2015, 5, 1)]

        result = ds.date_range(2015, 1, 2015, 5)
        self.assertEquals(result, expected)

if __name__ == "__main__":
    unittest.main()