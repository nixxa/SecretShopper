import unittest
from frontui.views import annual_month

class TestAnnualReport(unittest.TestCase):
    """ Test Case for annual report """
    def test_report_august(self):
        """ test august report """
        date = '20160801'
        annual_month(date)
        return


if __name__ == '__main__':
    unittest.main()