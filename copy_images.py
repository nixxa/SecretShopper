''' Copy images for export '''
from argparse import ArgumentParser
from frontui.data_provider import DataProvider
from frontui.views.member import calculate_date_period
from frontui.linq import where,select
from datetime import datetime
import os
import shutil

parser = ArgumentParser()
parser.add_argument(dest="destination")
parser.add_argument("-d", "--date", dest="date")
args = parser.parse_args()

date = datetime.strptime(args.date, '%Y-%m-%d')
(start_date, end_date) = calculate_date_period(date)
print('StartDate %s' % start_date.strftime('%Y-%m-%d'))
print('EndDate %s' % end_date.strftime('%Y-%m-%d'))

database = DataProvider()
checklists = where(database.checklists, lambda x: x.state == 'verified' and x.date > start_date and x.date < end_date)
objects = list(set(select(checklists, lambda x: x.object_info.num)))
for obj in objects:
    reports_list = sorted(where(checklists, lambda x: x.object_info.num == obj), key=lambda x: x.date)
    for indx, rprt in enumerate(reports_list, start=1):
        dirdest = os.path.join(args.destination, obj + '_' + str(indx))
        print('Copy to %s' % dirdest)
        if not os.path.exists(dirdest):
            os.makedirs(dirdest)
        for fdesc in rprt.files:
            filepath = fdesc['local_path']
            filedest = os.path.join(dirdest, fdesc['filename'])
            try:
                shutil.copy(filepath, filedest)
            except Exception as err:
                print(err)
