""" Checklist preparation and editing """
#pylint: disable=line-too-long

import uuid
import os
from datetime import datetime
from flask import render_template, request, Blueprint, current_app, session, send_file
from werkzeug.utils import secure_filename
from frontui.data_provider import DataProvider
from frontui.linq import first_or_default
from frontui.sendmail import MailProvider
from frontui.views import ALLOWED_EXTENSIONS, IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, EXCEL_EXTENSIONS


public_ui = Blueprint('ui', __name__)

@public_ui.route('/')
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


@public_ui.route('/checklist/<num>')
def checklist(num):
    """Renders questionnaire page"""
    database = DataProvider()
    objects = database.objects
    selected_obj = next((x for x in objects if x.num == num), None)
    questions = database.checklist
    return render_template(
        'checklist.html',
        objects=objects,
        selected=selected_obj,
        checklist=questions,
        title='Контрольный лист посещения | Тайный покупатель'
    )


@public_ui.route('/checklist/new', methods=['POST'])
def checklist_new():
    """ Save questionnaire and render success page """
    database = DataProvider()
    objects = database.objects
    object_num = request.form['object_name']
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
    session['checklist-uid'] = data['uid']
    return render_template(
        'checklist_addfiles.html',
        uid=data['uid'],
        object_name=selected_obj.num + '-' + selected_obj.title,
        save_date=data['create_date'],
        files=list(),
        notice_sent=False,
        title='Контрольный лист посещения | Тайный покупатель'
    )


@public_ui.route('/checklist/view/<uid>')
@public_ui.route('/checklist/addfiles/<uid>')
def checklist_addfiles(uid):
    """ View saved checklist by ID """
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    session['checklist-uid'] = uid
    return render_template(
        'checklist_addfiles.html',
        uid=uid,
        object_name=item.object_info.num + '-' + item.object_info.title,
        save_date=item.date,
        files=item.files,
        notice_sent=item.notice_sent,
        title='Контрольный лист посещения | Тайный покупатель'
    )


@public_ui.route('/checklist/edit/<uid>')
def checklist_edit(uid):
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
        edit_mode='edit',
        title='Контрольный лист посещения | Тайный покупатель'
    )


@public_ui.route('/checklist/save', methods=['POST'])
def checklist_save():
    """ Save verified checklist """
    database = DataProvider()
    data = dict()
    for key in request.form:
        data[key] = request.form[key]
    uid = data['uid']
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    if item.state == 'new':
        item.update(data)
        item.verify_date = datetime.utcnow()
        database.update_checklist(item)
    return render_template(
        'checklist_addfiles.html',
        uid=uid,
        object_name=item.object_info.num + '-' + item.object_info.title,
        save_date=item.date,
        files=item.files,
        notice_sent=item.notice_sent,
        title='Контрольный лист посещения | Тайный покупатель'
    )


@public_ui.route('/checklist/complete/<uid>', methods=['POST'])
def checklist_complete(uid):
    """ Complete checklist and send email configrmation """
    email = request.form['author_email']
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    if not item.notice_sent:
        mail = MailProvider()
        mail.send_checklist_notice(email, item)
        item.notice_sent = True
        # update checklist in DB
        database.update_checklist(item)
    return '', 200


@public_ui.route('/file/upload', methods=['POST'])
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
    if not file or file.filename == '':
        return 'No selected file', 500
    if not allowed_file(file.filename):
        return 'File %s is not allowed' % file.filename, 500
    filename = secure_filename(file.filename)
    # create dir for checklist
    filedir = database.get_uploads_dir(item)
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
    file_info['size'] = os.path.getsize(filepath)
    file_info['remote_path'] = ''
    if image_file(filename):
        file_info['filetype'] = 'image'
    elif audio_file(filename):
        file_info['filetype'] = 'audio'
    else:
        file_info['filetype'] = 'document'
    # update checklist in DB
    database.update_checklist(item)
    return '', 200


@public_ui.route('/uploads/<uid>/<filename>')
def view_file(uid, filename):
    """ Return saved filename """
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    if item is None:
        return 'File not exists', 404
    file_info = first_or_default(item.files, lambda x: x['filename'] == filename)
    if file_info is None:
        return 'File not exists', 404
    local_path = file_info['local_path'].replace('./frontui/', '').replace('\\', '/')
    return send_file(local_path)


@public_ui.route('/uploads/remove/<uid>/<filename>', methods=['POST'])
def remove_file(uid, filename):
    """ Remove file from checklist """
    database = DataProvider()
    item = first_or_default(database.checklists, lambda x: x.uid == uid)
    if item is None:
        return 'File not exists', 404
    file_info = first_or_default(item.files, lambda x: x['filename'] == filename)
    if file_info is None:
        return 'File not exists', 404
    item.files.remove(file_info)
    os.remove(file_info['local_path'])
    database.update_checklist(item)
    return '', 200


def allowed_file(filename):
    fext = os.path.splitext(filename)[1].lower()
    return fext in ALLOWED_EXTENSIONS


def image_file(filename):
    fext = os.path.splitext(filename)[1].lower()
    return fext in IMAGE_EXTENSIONS


def audio_file(filename):
    fext = os.path.splitext(filename)[1].lower()
    return fext in AUDIO_EXTENSIONS
