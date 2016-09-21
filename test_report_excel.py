import unittest
from datetime import datetime
from frontui.linq import first_or_default
from frontui.models import Checklist
from frontui.data_provider import DataProvider
from frontui.views.member import calc_points, add_one_month
from openpyxl import load_workbook

class TestUserActionInfo(unittest.TestCase):
    """ Test case """
    def calc_report(self, num, date):
        """
        Create report
        :type num: str
        :type date: str
        :rtype: models.Checklist
        """
        start_date = datetime.strptime(date, '%Y%m%d')
        end_date = add_one_month(start_date)
        database = DataProvider()
        object_info = first_or_default(database.objects, lambda x: x.num == num)
        rprt = first_or_default(database.checklists, lambda x: x.object_info.num == num and x.date >= start_date and x.date < end_date)
        calc_points(rprt, object_info)
        return rprt

    def save_excel(self, num, date):
        """
        Test save excel report
        """
        database = DataProvider()
        checklist = database.checklist
        report = self.calc_report(num, date)
        workbook = load_workbook(filename='./frontui/app_data/valar_report_tmpl.xlsx')
        worksheet = workbook.active
        cells = worksheet.get_named_range('azs%s_1' % num)
        cells[0].value = report.date.strftime('%d.%m.%Y')
        cells[1].value = report.get('p1_r2')
        cells[2].value = report.get('p1_r3')
        cells[3].value = report.get('p1_r4')
        cells[4].value = report.get('p1_r5')
        cells[5].value = 'ТП'
        cells[6].value = report.get('operator_fullname')
        if report.object_info.with_cafe:
            cells[7].value = report.get('accounter_fullname') + ' / ' + report.get('accounter_cafe_fullname')
        else:
            cells[7].value = report.get('accounter_fullname')
        index = 8
        for page_index, page in enumerate(checklist.pages):
            if page_index >= 8 or page_index == 0:
                continue
            cells[index].value = report.sum_points(page)
            index += 1
            for q in page.questions:
                cells[index].value = report.get_points(q.field_name, q)
                index += 1
        cells[index].value = report.max_points
        index += 1
        cells[index].value = report.points
        index += 1
        cells[index].value = report.points_percent
        # save workbook
        workbook.save(filename='./frontui/app_data/report_%s_%s.xlsx' % (num, date))
        return

    def test_excel(self):
        self.save_excel('4', '20160801')
        return

if __name__ == '__main__':
    unittest.main()