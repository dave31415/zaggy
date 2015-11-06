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

    def test_date_to_number(self):
        date = datetime.date(2015, 2, 15)
        number = ds.date_to_number(date)
        self.assertEquals(number, 1423958400.0)
        date = datetime.date(1970, 1, 1)
        number = ds.date_to_number(date)
        self.assertEquals(number, 0)

if __name__ == "__main__":
    unittest.main()