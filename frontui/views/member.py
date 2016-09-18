""" Reports, administration """
#pylint: disable=line-too-long

from datetime import datetime, timedelta
from flask import render_template, request, Blueprint, redirect
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
    new_checklists = dict()
    # fill all checklists
    for item in database.checklists:
        num = item.object_info.num
        if num not in checklists:
            checklists[num] = list()
        checklists[num].append(item)
    # fill only new checklists
    for item in [x for x in database.checklists if x.state == 'new']:
        num = item.object_info.num
        if num not in new_checklists:
            new_checklists[num] = list()
        new_checklists[num].append(item)
    return render_template(
        'reports.html',
        objects=objects,
        checklists=checklists,
        new_checklists=new_checklists,
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
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
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
    """ Render annual month report """
    rprt = dict()
    database = DataProvider()
    start_date = datetime.strptime(date, '%Y%m%d')
    end_date = add_one_month(start_date)
    rprt['checklist'] = database.checklist
    rprt['date'] = start_date
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
    """ Return date more then specified on one month """
    dt1 = dt0.replace(day=1)
    dt2 = dt1 + timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3


def calc_points(rprt, object_info):
    """ Calculate points for report """
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