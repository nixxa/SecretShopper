"""
Routes and views for the flask application.
"""
# pylint: disable=line-too-long

import uuid
import os
from datetime import datetime
from flask import render_template, request, Blueprint, current_app, redirect, session
from flask.ext.mobility.decorators import mobile_template
from werkzeug import secure_filename
from werkzeug.local import LocalProxy
from frontui.view_models import QListViewModel
from frontui.data_provider import DataProvider
from frontui.auth import authorize
from frontui.linq import first_or_default


ui = Blueprint('ui', __name__, template_folder='templates')
logger = LocalProxy(lambda: current_app.logger)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@ui.route('/')
def home():
    """Renders the home page."""
    database = DataProvider()
    objects = database.objects
    return render_template(
        'index.html',
        title='Список объектов|Тайный покупатель',
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
        title='Контрольный лист посещения|Тайный покупатель'
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
    return render_template(
        template,
        model=model,
        title='Контрольны лист посещения|Тайный покупатель'
    )


@ui.route('/checklist/view/<uid>')
@mobile_template('{mobile/}checklist_saved.html')
def checklist_view(template, uid):
    """ View saved checklist by ID """
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    session['checklist-uid'] = uid
    model = QListViewModel()
    model.num = uid
    model.object_name = item.object_info.num + '-' + item.object_info.title
    return render_template(
        template,
        model=model,
        title='Контрольный лист посещения|Тайный покупатель'
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
        filedir = os.path.join(current_app.config['UPLOAD_FOLDER'], uid)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        file.save(os.path.join(filedir, filename))
    return '', 200


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@ui.route('/reports')
@mobile_template('{mobile/}reports.html')
@authorize
def reports(template):
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
        template,
        objects=objects,
        checklists=checklists,
        new_checklists=new_checklists,
        title='Отчеты'
    )


@ui.route('/reports/<obj_num>')
@mobile_template('{mobile/}reports_by_object.html')
@authorize
def reports_by_object(template, obj_num):
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
        template,
        selected=selected_obj,
        checklists=checklists,
        new_checklists=new_checklists,
        title='Отчеты'
    )


@ui.route('/report/<uid>')
@mobile_template('{mobile/}report.html')
@authorize
def report(template, uid):
    """ Render object report for verify """
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    questions = database.checklist
    return render_template(
        template,
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
