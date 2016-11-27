""" Reports, administration """
#pylint: disable=line-too-long

import logging
import os
from datetime import datetime, timedelta
from flask import render_template, request, Blueprint, redirect, session, send_file
from frontui import BASE_DIR
from frontui.data_provider import DataProvider
from frontui.auth import authorize
from frontui.linq import first_or_default, where, count, select, order_by
from frontui.sendmail import MailProvider
from openpyxl import load_workbook
from openpyxl.comments import Comment
from openpyxl.utils.exceptions import NamedRangeException


member_ui = Blueprint('member', __name__)
logger = logging.getLogger(__name__)


@member_ui.route('/reports')
@authorize
def reports():
    """
    Отчеты по объектам
    """
    database = DataProvider()
    objects = database.objects
    checklists = dict()
    # fill all checklists
    for item in database.checklists:
        num = item.object_info.num
        if num not in checklists:
            checklists[num] = list()
        checklists[num].append(item)
    current_user = session['user_name']
    new_from_last_visit = dict()
    # fill only new checklists (not seen by someone)
    new_checklists = dict()
    visited_checklists = dict()
    for item in [x for x in database.checklists if x.state == 'new']:
        num = item.object_info.num
        if current_user not in item.visited_by:
            new_from_last_visit[num] = True
        else:
            if num in new_from_last_visit:
                new_from_last_visit[num] = False or new_from_last_visit[num]
            else:
                new_from_last_visit[num] = False
        if num not in new_checklists:
            new_checklists[num] = list()
            visited_checklists[num] = list()
        if len(item.visited_by) == 0:
            new_checklists[num].append(item)
        else:
            visited_checklists[num].append(item)
    # render template
    return render_template(
        'reports.html',
        objects=objects,
        checklists=checklists,
        new_checklists=new_checklists,
        staged_checklists=visited_checklists,
        new_from_last_visit=new_from_last_visit,
        title='Отчеты'
    )


@member_ui.route('/reports/<obj_num>')
@authorize
def reports_by_object(obj_num):
    """ Render reports for object """
    database = DataProvider()
    objects = database.objects
    selected_obj = first_or_default(objects, lambda x: x.num == obj_num)
    checklists = list()
    new_checklists = list()
    # fill all checklists
    for item in [x for x in database.checklists if x.state != 'new']:
        num = item.object_info.num
        if num == obj_num:
            checklists.append(item)
    # fill only new checklists
    for item in [x for x in database.checklists if x.state == 'new']:
        num = item.object_info.num
        if num == obj_num:
            new_checklists.append(item)
    return render_template(
        'reports_by_object.html',
        selected=selected_obj,
        checklists=checklists,
        new_checklists=new_checklists,
        title='Отчеты'
    )


@member_ui.route('/report/<uid>')
@authorize
def report(uid):
    """ Render object report for verify """
    database = DataProvider()
    # get checklist and show it in edit mode
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    item.visit_by(session['user_name'])
    database.update_checklist(item)
    questions = database.checklist
    return render_template(
        'checklist_edit.html',
        values=item,
        checklist=questions,
        selected=item.object_info,
        objects=database.objects,
        edit_mode='verify',
        title='Отчет'
    )


@member_ui.route('/report/verify', methods=['POST'])
@authorize
def verify():
    """ Save verified checklist """
    database = DataProvider()
    data = dict()
    for key in request.form:
        data[key] = request.form[key]
    uid = data['uid']
    obj = first_or_default(database.checklists, lambda x: x.uid == uid)
    obj.update(data)
    obj.state = 'verified'
    obj.verify_date = datetime.utcnow()
    database.update_checklist(obj)
    mail_sender = MailProvider()
    mail_sender.send_checklist_verified(obj)
    return redirect('/reports')


@member_ui.route('/report/remove/<uid>')
@authorize
def remove_report(uid):
    """
    Remove checklist and it's files completely
    """
    database = DataProvider()
    # get checklist and show it in edit mode
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    if item is None:
        return redirect('/reports')
    obj_num = item.object_info.num
    database.remove_checklist(checklist=item)
    return redirect('/reports/%s' % obj_num)


@member_ui.route('/report/changemonth', methods=['POST'])
@authorize
def change_month():
    """ Change date of checklist """
    uid = request.form['uid']
    new_month = int(request.form['month'])
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    item.date = item.date.replace(month=new_month).replace(day=10)
    database.update_checklist(item)
    return '', 200


@member_ui.route('/annual/all')
@authorize
def annual_reports():
    """ Return list of all existing annual reports """
    database = DataProvider()
    total = count(database.objects, lambda x: x.with_cafe) * 2 + \
            count(database.objects, lambda x: not x.with_cafe)
    reports_list = list()
    # calculate count of annual reports
    items = sorted(database.checklists, key=lambda x: x.date)
    start_date = items[0].date.replace(day=1)
    now_date = datetime.now()
    while start_date < now_date:
        next_date = add_one_month(start_date)
        (shifted_start, shifted_end) = calculate_date_period(start_date)
        all_records = where(items, lambda x: x.date > shifted_start and x.date < shifted_end)
        logger.info('All records between %s and %s: %s', shifted_start.strftime('%Y-%m-%d'), shifted_end.strftime('%Y-%m-%d'), len(all_records))
        if len(all_records) == 0:
            # roll to next month
            start_date = next_date
            continue
        verified = where(all_records, lambda x: x.state == 'verified')
        logger.info('Verified records between %s and %s: %s', shifted_start.strftime('%Y-%m-%d'), shifted_end.strftime('%Y-%m-%d'), len(verified))
        report_item = dict()
        report_item['date'] = start_date
        report_item['all'] = len(all_records)
        report_item['verified'] = len(verified)
        report_item['total'] = total
        reports_list.append(report_item)
        # roll to next month
        start_date = next_date
    return render_template(
        'annual_list.html',
        model=reports_list,
        title='Отчеты'
    )


@member_ui.route('/annual/<date>')
@authorize
def annual_month(date):
    """
    Render annual month report
    :type date: str
    """
    rprt = dict()
    database = DataProvider()
    # calculate start date as week before 1 day of current month, if 1 day not Monday
    (start_date, end_date) = calculate_date_period(date)
    logger.debug('StartDate %s', start_date.strftime('%Y-%m-%d'))
    logger.debug('EndDate %s', end_date.strftime('%Y-%m-%d'))
    rprt['checklist'] = database.checklist
    rprt['date'] = datetime.strptime(date, '%Y%m%d')
    # load all checklists within dates range
    checklists = where(database.checklists,
                       lambda x: x.state == 'verified' and x.date > start_date and x.date < end_date)
    # set object's collections
    collection = select(
        where(checklists, lambda x: not x.object_info.with_cafe and not x.object_info.with_shop),
        lambda xx: xx.object_info)
    rprt['kiosks'] = sorted(list(set(collection)), key=lambda xxx: xxx.sort_num)
    rprt['kiosks_count'] = len(rprt['kiosks'])
    rprt['kiosks_columns'] = len(collection)
    # set shops
    collection = select(
        where(checklists, lambda x: x.object_info.with_shop and not x.object_info.with_cafe),
        lambda xx: xx.object_info)
    rprt['shops'] = sorted(list(set(collection)), key=lambda xxx: xxx.sort_num)
    rprt['shops_count'] = len(rprt['shops'])
    rprt['shops_columns'] = len(collection)
    # set cafes
    collection = select(
        where(checklists, lambda x: x.object_info.with_cafe),
        lambda xx: xx.object_info)
    rprt['cafes'] = sorted(list(set(collection)), key=lambda xxx: xxx.sort_num)
    rprt['cafes_count'] = len(rprt['cafes'])
    rprt['cafes_columns'] = len(collection)
    # calculate points
    for item in rprt['kiosks']:
        rprt[item.num] = where(checklists, lambda x: x.object_name == item.num)
        for report_item in rprt[item.num]:
            calc_points(report_item)
    for item in rprt['shops']:
        rprt[item.num] = sorted(
            where(checklists, lambda x: x.object_name == item.num),
            key=lambda x: x.date)
        for report_item in rprt[item.num]:
            calc_points(report_item)
    for item in rprt['cafes']:
        rprt[item.num] = sorted(
            where(checklists, lambda x: x.object_name == item.num),
            key=lambda x: x.date)
        for report_item in rprt[item.num]:
            calc_points(report_item)
    return render_template(
        'annual_month.html',
        model=rprt,
        title='Отчет за {0}'.format(start_date.strftime('%B %Y'))
    )


@member_ui.route('/annual/excel/<date>')
@authorize
def annual_excel_month(date):
    """
    Save report as excel file and return it
    :type date: str
    """
    database = DataProvider()
    # calculate start date as week before 1 day of current month, if 1 day not Monday
    (start_date, end_date) = calculate_date_period(date)
    logger.debug('StartDate %s', start_date.strftime('%Y-%m-%d'))
    logger.debug('EndDate %s', end_date.strftime('%Y-%m-%d'))
    # generate report
    workbook = load_workbook(os.path.join(BASE_DIR, os.path.join('app_data', get_report_template(start_date))))
    worksheet = workbook.worksheets[0]
    checklists = where(database.checklists,
                       lambda x: x.state == 'verified' and x.date > start_date and x.date < end_date)
    objects = list(set(select(checklists, lambda x: x.object_info.num)))
    for obj in objects:
        reports_list = sorted(where(checklists, lambda x: x.object_info.num == obj), key=lambda x: x.date)
        for indx, rprt in enumerate(reports_list, start=1):
            calc_points(rprt)
            range_name = 'azs%s_%s' % (obj.replace('-', '_'), indx)
            try:
                cells = worksheet.get_named_range(range_name)
                fill_cells(rprt, cells)
            except NamedRangeException as nre:
                logger.debug('Error while trying to get named range \'%s\'', range_name)
    workbook.save(os.path.join(BASE_DIR, 'files/report_%s.xlsx' % date))
    return send_file('./files/report_%s.xlsx' % date, mimetype='application/excel', as_attachment=True, attachment_filename='report_%s.xlsx' % date)


def get_report_template(report_date):
    """
    Return filename for current template
    :type report_date: datetime
    :rtype: str
    """
    if report_date >= datetime(year=2016, month=9, day=1):
        logger.info('Using new template: valar_report_tmpl_20161001.xlsx')
        return 'valar_report_tmpl_20161001.xlsx'
    logger.info('Using template: valar_report_tmpl.xlsx')
    return 'valar_report_tmpl.xlsx'


def get_shops_count(report_date, objects):
    """
    Return checklists count for azs with shops
    """
    if report_date >= datetime(year=2016, month=9, day=1):
        return 2 * len(objects)
    return len(objects)


def add_one_month(dt0):
    """
    Return date more then specified on one month
    :type dt0: datetime
    :rtype: datetime
    """
    dt1 = dt0.replace(day=1)
    dt2 = dt1 + timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3


def calculate_date_period(*args):
    """
    Calculate start and end dates of given month
    :rtype:tuple of 2 dates
    """
    # calculate start date as week before first monday in month
    month = args[0]
    if len(args) == 1 and isinstance(args[0], str):
        month = datetime.strptime(args[0], '%Y%m%d')
    start_date = datetime(year=month.year, month=month.month, day=1)
    if start_date.isoweekday() != 1:
        # shift to first monday
        start_date = start_date + timedelta(days=(8 - start_date.isoweekday()))
    # shift to week before
    start_date = start_date - timedelta(days=7)
    # calculate end date as week before first monday in next month
    end_date = datetime(year=month.year, month=month.month, day=1) + timedelta(days=32)
    end_date = end_date.replace(day=1)
    if end_date.isoweekday() != 1:
        # shift to first monday
        end_date = end_date + timedelta(days=(8 - end_date.isoweekday()))
        # shift to week before
        end_date = end_date - timedelta(days=7)
    return (start_date, end_date)


def calc_points(rprt):
    """
    Calculate points for report
    :type rprt: models.Checklist
    :rtype: models.Checklist
    """
    database = DataProvider()
    object_info = rprt.object_info
    points = 0
    max_points = 0
    for i in range(1, 8):
        page = database.checklist.pages[i]
        max_points = max_points + page.max_cost(object_info)
        for question in page.questions:
            answer = rprt.get(question.field_name)
            if answer is None:
                answer = 'n/a'
            answer_yes = answer == 'yes'
            if not object_info.applies(question):
                continue
            if question.optional and answer == 'n/a' and not object_info.num in question.excepts:
                max_points = max_points - page.cost
            points = points + (page.cost if answer_yes else 0)
    rprt.max_points = max_points
    rprt.points = points
    rprt.points_percent = points/max_points*100
    return rprt


def fill_cells(rprt, cells):
    """
    Fill report cells with data
    """
    database = DataProvider()
    checklist = database.checklist
    cells[0].value = rprt.date.strftime('%d.%m.%Y')
    cells[1].value = rprt.get('p1_r2')
    cells[2].value = rprt.get('p1_r3')
    cells[3].value = rprt.get('p1_r4')
    cells[4].value = rprt.get('p1_r5')
    cells[5].value = 'ТП'
    cells[6].value = rprt.get('operator_fullname')
    if rprt.object_info.with_cafe:
        cells[7].value = rprt.get('accounter_fullname') + ' / ' + rprt.get('accounter_cafe_fullname')
    else:
        cells[7].value = rprt.get('accounter_fullname')
    index = 8
    for page_index, page in enumerate(checklist.pages):
        if page_index >= 8 or page_index == 0:
            continue
        #sum cell included in template
        #cells[index].value = rprt.sum_points(page)
        index += 1
        for question in page.questions:
            cell_value = rprt.get_points(question.field_name, question)
            cells[index].value = cell_value
            if question.child is not None and (cell_value is None or cell_value == 0):
                # insert comment, cause question has description in some cases
                comment_value = rprt.get(question.child.field_name)
                if comment_value != '' and comment_value is not None:
                    cells[index].comment = Comment(rprt.get(question.child.field_name), 'Author')
            index += 1
    cells[index].value = rprt.max_points
    index += 1
    #sum cell included in template
    #cells[index].value = rprt.points
    index += 1
    #precent cell included in template
    #cells[index].value = rprt.points_percent
    index += 1
    cells[index].value = rprt.get('p8_r1')
    index += 1
    cells[index].value = rprt.get('p8_r5')
    index += 1
    cells[index].value = rprt.get('p8_r6')
    index += 1
    cells[index].value = rprt.get('p8_r7')
    index += 1
    cells[index].value = rprt.get('p8_r3')
    index += 1
    cells[index].value = rprt.get('p9_r1')
    if rprt.get('p9_r2') != '':
        cells[index].comment = Comment(rprt.get('p9_r2'), 'Author')
    return cells
