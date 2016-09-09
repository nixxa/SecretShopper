"""
Routes and views for the flask application.
"""
# pylint: disable=line-too-long

import uuid
import os
import sys
from datetime import datetime, timedelta
from flask import render_template, request, Blueprint, current_app, redirect, session, send_file
from flask.ext.mobility.decorators import mobile_template
from werkzeug import secure_filename
from werkzeug.local import LocalProxy
#from PIL import Image
from frontui.view_models import QListViewModel
from frontui.data_provider import DataProvider
from frontui.auth import authorize
from frontui.linq import first_or_default, where, count


ui = Blueprint('ui', __name__, template_folder='templates')
logger = LocalProxy(lambda: current_app.logger)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF', 'm4a', 'wav', 'mp3', 'ogg', '3gpp', 'mp4'])
IMAGE_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF'])
AUDIO_EXTENSIONS = set(['m4a', 'wav', 'mp3', 'ogg', '3gpp', 'mp4'])

@ui.route('/')
def home():
    """Renders the home page."""
    database = DataProvider()
    objects = database.objects
    return render_template(
        'index.html',
        title='Список объектов | Тайный покупатель',
        objects=objects,
        year=datetime.now().year,
    )


@ui.route('/checklist/<num>')
@mobile_template('{mobile/}checklist.html')
def checklist(template, num):
    """Renders questionnaire page"""
    database = DataProvider()
    objects = database.objects
    selected_obj = next((x for x in objects if x.num == num), None)
    questions = database.checklist
    return render_template(
        template,
        objects=objects,
        selected=selected_obj,
        checklist=questions,
        title='Контрольный лист посещения | Тайный покупатель'
    )


@ui.route('/save_list', methods=['POST'])
@mobile_template('{mobile/}checklist_saved.html')
def checklist_save(template):
    """ Save questionnaire and render success page """
    database = DataProvider()
    objects = database.objects
    object_num = request.form['object_name']
    logger.debug('ObjectNum %s' % object_num)
    selected_obj = next((x for x in objects if x.num == object_num), None)
    selected_date = request.form['p1_r1']
    data = dict()
    data['uid'] = str(uuid.uuid4())
    data['state'] = 'new'
    data['create_date'] = datetime.utcnow()
    data['verify_date'] = None
    for key in request.form:
        data[key] = request.form[key]
    database.save_checklist(object_num, selected_date, data)
    model = QListViewModel()
    model.num = data['uid']
    model.object_name = selected_obj.num + '-' + selected_obj.title
    session['checklist-uid'] = model.num
    return render_template(
        template,
        model=model,
        title='Контрольны лист посещения | Тайный покупатель'
    )


@ui.route('/checklist/view/<uid>')
def checklist_view(uid):
    """ View saved checklist by ID """
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    session['checklist-uid'] = uid
    model = QListViewModel()
    model.num = uid
    model.object_name = item.object_info.num + '-' + item.object_info.title
    model.save_date = item.date
    return render_template(
        'checklist_saved.html',
        model=model,
        title='Контрольный лист посещения | Тайный покупатель'
    )


@ui.route('/file/upload', methods=['POST'])
def upload():
    """ Upload and save file """
    uid = session['checklist-uid']
    if uid is None:
        return 'No active checklist', 500
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part', 500
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return 'No selected file', 500
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # create dir for checklist
        filedir = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            item.date.strftime('%Y'),
            item.date.strftime('%m'),
            item.object_info.num,
            uid)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filepath = os.path.join(filedir, filename)
        file.save(filepath)
        # save file info in checklist
        if item.files is None:
            item.files = list()
        file_info = first_or_default(item.files, lambda x: x['filename'] == filename)
        if file_info is None:
            file_info = dict()
            item.files.append(file_info)
        file_info['filename'] = filename
        file_info['local_path'] = filepath
        file_info['remote_path'] = ''
        if image_file(filename):
            file_info['filetype'] = 'image'
        elif audio_file(filename):
            file_info['filetype'] = 'audio'
        # update checklist in DB
        database.update_checklist(item)
    return '', 200


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in IMAGE_EXTENSIONS


def audio_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in AUDIO_EXTENSIONS


@ui.route('/uploads/<uid>/<filename>')
@authorize
def view_file(uid, filename):
    """ Return saved filename """
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    if item is None:
        return 'File not exists', 404
    file_info = first_or_default(item.files, lambda x: x['filename'] == filename)
    if file_info is None:
        return 'File not exists', 404
    local_path = file_info['local_path'].replace('./frontui/', '')
    return send_file(local_path)


@ui.route('/reports')
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


@ui.route('/reports/<obj_num>')
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


@ui.route('/report/<uid>')
@authorize
def report(uid):
    """ Render object report for verify """
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    questions = database.checklist
    return render_template(
        'report.html',
        values=item,
        checklist=questions,
        selected=item.object_info,
        objects=database.objects,
        title='Отчет'
    )


@ui.route('/report/verify', methods=['POST'])
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


@ui.route('/annual/all')
@authorize
def annual_reports():
    """ Return list of all existing annual reports """
    database = DataProvider()
    total = count(database.objects, lambda x: x.with_cafe == True) * 2 + \
            count(database.objects, lambda x: x.with_cafe == False)
    reports = list()
    # calculate count of annual reports
    items = sorted(database.checklists, key=lambda x: x.date)
    start_date = items[0].date.replace(day=1)
    now_date = datetime.now()
    while start_date < now_date:
        next_date = add_one_month(start_date)
        all = where(items, lambda x: x.date >= start_date and x.date < next_date)
        verified = where(all, lambda x: x.state == 'verified')
        report = dict()
        report['date'] = start_date
        report['all'] = len(all)
        report['verified'] = len(verified)
        report['total'] = total
        reports.append(report)
        # roll to next month
        start_date = next_date
    return render_template('annual_list.html', model=reports)


def add_one_month(dt0):
    dt1 = dt0.replace(day=1)
    dt2 = dt1 + timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3


@ui.route('/annual/<date>')
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
    return render_template('annual_month.html', model=rprt)


def calc_points(rprt, object_info):
    """ Calculate points for report """
    database = DataProvider()
    p = 0
    m = 0
    for i in range(1,8):
        pg = database.checklist.pages[i]
        m = m + pg.max_cost(object_info)
        for q in pg.questions:
            answer = rprt.get(q.field_name) == 'yes'
            if q.optional and rprt.get(q.field_name) == 'n/a' and not object_info.num in q.excepts: 
                m = m -  pg.cost
            p = p + (pg.cost if answer else 0)
    rprt.max_points = m
    rprt.points = p
    rprt.points_percent = p/m*100
    return rprt
