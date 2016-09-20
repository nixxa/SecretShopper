""" Reports, administration """
#pylint: disable=line-too-long

import logging
from datetime import datetime, timedelta
from flask import render_template, request, Blueprint, redirect, session
from frontui.data_provider import DataProvider
from frontui.auth import authorize
from frontui.linq import first_or_default, where, count

member_ui = Blueprint('member', __name__)

@member_ui.route('/reports')
@authorize
def reports():
    """ Отчеты по объектам """
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
        all_records = where(items, lambda x: x.date >= start_date and x.date < next_date)
        if len(all_records) == 0:
            # roll to next month
            start_date = next_date
            continue
        verified = where(all_records, lambda x: x.state == 'verified')
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
    month = datetime.strptime(date, '%Y%m%d')
    # calculate start date as week before 1 day of current month, if 1 day not Monday
    start_date = shift_start_date(month)
    logging.debug('StartDate %s', start_date.strftime('%Y-%m-%d'))
    # calculate end date as week before 1day of next month, if 1 day not Monday
    end_date = shift_end_date(add_one_month(month))
    logging.debug('EndDate %s', end_date.strftime('%Y-%m-%d'))
    rprt['checklist'] = database.checklist
    rprt['date'] = month
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
        lambda x: x.state == 'verified' and x.date >= start_date and x.date < end_date)
    for item in rprt['kiosks']:
        rprt[item.num] = where(checklists, lambda x: x.object_name == item.num)
        for x in rprt[item.num]:
            calc_points(x, item)
    for item in rprt['shops']:
        rprt[item.num] = sorted(
            where(checklists, lambda x: x.object_name == item.num),
            key=lambda x: x.date)
        for x in rprt[item.num]:
            calc_points(x, item)
    for item in rprt['cafes']:
        rprt[item.num] = sorted(
            where(checklists, lambda x: x.object_name == item.num),
            key=lambda x: x.date)
        for x in rprt[item.num]:
            calc_points(x, item)
    return render_template(
        'annual_month.html',
        model=rprt,
        title='Отчет за {0}'.format(start_date.strftime('%B %Y'))
    )


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

def shift_start_date(dt):
    """
    Shift date for 1 week, if it is first day of month and not Monday
    :type dt: datetime
    :rtype: datetime
    """
    if dt.day != 1:
        return dt
    if dt.isoweekday() != 1:
        dt = dt - timedelta(days=7)
    return dt

def shift_end_date(dt):
    """
    Shift date for 1 week, if it is first day of month and not Monday
    :type dt: datetime
    :rtype: datetime
    """
    if dt.day != 1:
        return dt
    if dt.isoweekday() != 1:
        shift = 8 - dt.isoweekday()
        dt = dt + timedelta(days=shift)
        dt = dt - timedelta(days=8)
    return dt

def calc_points(rprt, object_info):
    """
    Calculate points for report
    :type rprt: models.Checklist
    :type object_info: models.ObjectInfo
    :rtype: models.Checklist
    """
    database = DataProvider()
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
