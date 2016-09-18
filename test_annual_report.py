import unittest
from datetime import datetime
from frontui.linq import first_or_default
from frontui.data_provider import DataProvider
from frontui.views.member import calc_points, add_one_month

class TestAnnualReport(unittest.TestCase):
    """ Test Case for annual report """

    def calc_report(self, num, date):
        start_date = datetime.strptime(date, '%Y%m%d')
        end_date = add_one_month(start_date)
        database = DataProvider()
        object_info = first_or_default(database.objects, lambda x: x.num == num)
        rprt = first_or_default(database.checklists, lambda x: x.object_info.num == num and x.date >= start_date and x.date < end_date)
        calc_points(rprt, object_info)
        return rprt

    def test_applies_azs140(self):
        """ test applies questions for 140 """
        database = DataProvider()
        object_info = first_or_default(database.objects, lambda x: x.num == '140')
        page = database.checklist.pages[5]
        for q in page.questions:
            self.assertEqual(object_info.applies(q), False)
        return

    def test_report_august_azs6(self):
        """ test august report for azs 6 """
        date = '20160801'
        rprt = self.calc_report('6', date)
        self.assertEqual(rprt.max_points, 209)
        self.assertEqual(rprt.points, 182)
        return

    def test_report_august_azs140(self):
        """ test august report for azs 140 """
        date = '20160801'
        rprt = self.calc_report('140', date)
        self.assertEqual(rprt.max_points, 185)
        self.assertEqual(rprt.points, 165)
        return

    def test_report_august_azs1(self):
        """ test august report for azs 1 """
        date = '20160801'
        rprt = self.calc_report('1', date)
        self.assertEqual(rprt.max_points, 240)
        self.assertEqual(rprt.points, 230)
        return

    def test_report_august_azs5(self):
        """ test august report for azs 5 """
        date = '20160801'
        rprt = self.calc_report('5', date)
        self.assertEqual(rprt.max_points, 205)
        self.assertEqual(rprt.points, 198)
        return

    def test_report_august_azs22(self):
        """ test august report for azs 22 """
        date = '20160801'
        rprt = self.calc_report('22', date)
        self.assertEqual(rprt.max_points, 280)
        self.assertEqual(rprt.points, 266)
        return

    def test_report_august_azs83(self):
        """ test august report for azs 83 """
        date = '20160801'
        rprt = self.calc_report('83', date)
        self.assertEqual(rprt.max_points, 235)
        self.assertEqual(rprt.points, 208)
        return


if __name__ == '__main__':
    unittest.main()