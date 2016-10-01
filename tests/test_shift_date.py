import unittest
from context import calculate_date_period


class TestShiftDate(unittest.TestCase):

    def test_shift(self):
        # test august
        dates = calculate_date_period('20160801')
        self.assertEqual('20160725', dates[0].strftime('%Y%m%d'))
        self.assertEqual('20160829', dates[1].strftime('%Y%m%d'))
        # test september
        dates = calculate_date_period('20160901')
        self.assertEqual('20160829', dates[0].strftime('%Y%m%d'))
        self.assertEqual('20160926', dates[1].strftime('%Y%m%d'))
        # test october
        dates = calculate_date_period('20161001')
        self.assertEqual('20160926', dates[0].strftime('%Y%m%d'))
        self.assertEqual('20161031', dates[1].strftime('%Y%m%d'))
        return


if __name__ == '__main__':
    unittest.main()
