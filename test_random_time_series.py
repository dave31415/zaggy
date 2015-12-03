import unittest
from unittest import TestCase
import random_time_series as rts
import datetime
import numpy as np


class TestMakeDates(TestCase):
    """
        Test the make_dates function
    """
    def test_makes_right_number_of_dates(self):
        """
        Test that it makes an ndarray, that they are datetime objects
        and has right length
        :return: None
        """
        dates = rts.make_dates(15)
        self.assertTrue(isinstance(dates, np.ndarray))
        self.assertTrue(isinstance(dates[0], datetime.datetime))
        self.assertEquals(len(dates), 15)

    def test_exact_1_day(self):
        """
        Test that it returns expected results with 1 day cadence
        :return:
        """
        time_unit = (1, 'day')
        dates = rts.make_dates(3, time_unit=time_unit, start_date=None)
        expected = np.array([datetime.datetime(2015, 1, 1, 0, 0),
                             datetime.datetime(2015, 1, 2, 0, 0),
                             datetime.datetime(2015, 1, 3, 0, 0)], dtype=object)
        for d, e in zip(dates, expected):
            self.assertEquals(d, e)

    def test_exact_1_day_different_start_date(self):
        """
        Test that it returns expected results with 1 day cadence
        :return:
        """
        time_unit = (1, 'day')
        start_date = datetime.datetime(2016, 1, 1)
        dates = rts.make_dates(3, time_unit=time_unit, start_date=start_date)
        expected = np.array([datetime.datetime(2016, 1, 1, 0, 0),
                             datetime.datetime(2016, 1, 2, 0, 0),
                             datetime.datetime(2016, 1, 3, 0, 0)], dtype=object)
        for d, e in zip(dates, expected):
            self.assertEquals(d, e)

    def test_exact_2_months(self):
        """
        Test that it returns expected results with 2 month cadence
        :return:
        """
        time_unit = (2, 'months')
        dates = rts.make_dates(3, time_unit=time_unit, start_date=None)
        expected = np.array([datetime.datetime(2015, 1, 1, 0, 0),
                             datetime.datetime(2015, 3, 2, 21, 0),
                             datetime.datetime(2015, 5, 2, 18, 0)], dtype=object)
        for d, e in zip(dates, expected):
            self.assertEquals(d, e)


class TestMakeRandom(TestCase):
    """
        Test the make_random function
    """
    def test_make_random_works(self):
        """
        Check that it returns the right results with the right seed
        and a different answer with another seed
        :return: None
        """
        tol = 1e-7
        seed = 42
        y = rts.make_random(5, seed=seed)
        expected = np.array([0.49671415,  0.35844985,  1.00613839,
                             2.52916825,  2.29501487])

        for yy, e in zip(y, expected):
            diff = abs(yy - e)
            self.assertLess(diff, tol)

        # change seed, should change results
        seed = 99
        y = rts.make_random(5, seed=seed)
        expected = np.array([-0.14235884,  1.91486289,  2.19812484,
                             3.52793681,  3.37331496])

        for yy, e in zip(y, expected):
            diff = abs(yy - e)
            self.assertLess(diff, tol)


class TestRandomTS(TestCase):
    def test_return_values(self):
        t, y = rts.make_random_ts(5)
        self.assertEquals(len(t), 5)
        self.assertEquals(len(y), 5)

        self.assertTrue(isinstance(t, np.ndarray))
        self.assertTrue(isinstance(y, np.ndarray))
        self.assertTrue(isinstance(t[0], datetime.datetime))
        self.assertTrue(isinstance(y[0], np.float64))

if __name__ == "__main__":
    unittest.main()