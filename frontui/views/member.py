""" Reports, administration """
#pylint: disable=line-too-long

import logging
import os
from datetime import datetime, timedelta
from flask import render_template, request, Blueprint, redirect, session, send_file
from frontui import BASE_DIR
from frontui.data_provider import DataProvider
from frontui.auth import authorize
from frontui.linq import first_or_default, where, count, select
from openpyxl import load_workbook

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


@member_ui.route('/annual/all')
@authorize
def annual_reports():
    """ Return list of all existing annual reports """
    database = DataProvider()
    total = count(database.objects, lambda x: x.with_cafe == True) * 2 + \
            count(database.objects, lambda x: x.with_cafe == False)
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
    rprt['kiosks'] = sorted(
        where(database.objects, lambda x: x.with_shop == False and x.with_cafe == False),
        key=lambda x: x.sort_num)
    rprt['kiosks_count'] = len(rprt['kiosks'])
    rprt['shops'] = sorted(
        where(database.objects, lambda x: x.with_shop == True and x.with_cafe == False),
        key=lambda x: x.sort_num)
    rprt['shops_count'] = len(rprt['shops'])
    rprt['cafes'] = sorted(
        where(database.objects, lambda x: x.with_shop == True and x.with_cafe == True),
        key=lambda x: x.sort_num)
    rprt['cafes_count'] = 2 * len(rprt['cafes'])
    # initialize object's reports
    checklists = where(database.checklists, 
        lambda x: x.state == 'verified' and x.date > start_date and x.date < end_date)
    for item in rprt['kiosks']:
        rprt[item.num] = where(checklists, lambda x: x.object_name == item.num)
        for x in rprt[item.num]:
            calc_points(x)
    for item in rprt['shops']:
        rprt[item.num] = sorted(
            where(checklists, lambda x: x.object_name == item.num),
            key=lambda x: x.date)
        for x in rprt[item.num]:
            calc_points(x)
    for item in rprt['cafes']:
        rprt[item.num] = sorted(
            where(checklists, lambda x: x.object_name == item.num),
            key=lambda x: x.date)
        for x in rprt[item.num]:
            calc_points(x)
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
    workbook = load_workbook(os.path.join(BASE_DIR,'app_data/valar_report_tmpl.xlsx'))
    worksheet = workbook.active
    checklists = where(database.checklists, 
        lambda x: x.state == 'verified' and x.date > start_date and x.date < end_date)
    objects = select(checklists, lambda x: x.object_info.num)
    for obj in objects:
        reports = where(checklists, lambda x: x.object_info.num == obj)
        for indx, rprt in enumerate(reports, start=1):
            calc_points(rprt)
            cells = worksheet.get_named_range('azs%s_%s' % (obj.replace('-','_'), indx))
            fill_cells(rprt, cells)
    workbook.save(os.path.join(BASE_DIR, 'files/report_%s.xlsx' % date))
    return send_file('./files/report_%s.xlsx' % date, mimetype='application/excel', as_attachment=True, attachment_filename='report_%s.xlsx' % date)


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
    p = 0
    m = 0
    for i in range(1,8):
        pg = database.checklist.pages[i]
        m = m + pg.max_cost(object_info)
        for q in pg.questions:
            answer = rprt.get(q.field_name)
            if answer is None:
                answer = 'n/a'
            answer_yes = answer == 'yes'
            if not object_info.applies(q):
                continue
            if q.optional and answer == 'n/a' and not object_info.num in q.excepts: 
                m = m - pg.cost
            p = p + (pg.cost if answer_yes else 0)
    rprt.max_points = m
    rprt.points = p
    rprt.points_percent = p/m*100
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
        cells[index].value = rprt.sum_points(page)
        index += 1
        for q in page.questions:
            cells[index].value = rprt.get_points(q.field_name, q)
            index += 1
    cells[index].value = rprt.max_points
    index += 1
    cells[index].value = rprt.points
    index += 1
    cells[index].value = rprt.points_percent
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
    return cells