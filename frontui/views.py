"""
Routes and views for the flask application.
"""
# pylint: disable=line-too-long

import uuid
from datetime import datetime
from flask import render_template, request, Blueprint, current_app
from flask.ext.mobility.decorators import mobile_template
from werkzeug.local import LocalProxy
from frontui.view_models import QListViewModel
from frontui.data_provider import DataProvider

ui = Blueprint('ui', __name__, template_folder='templates')
logger = LocalProxy(lambda: current_app.logger)

@ui.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@ui.route('/checklist')
@mobile_template('{mobile/}checklist.html')
def checklist(template):
    """Renders questionnaire page"""
    database = DataProvider()
    objects = database.objects
    questions = database.checklist
    return render_template(
        template,
        objects=objects,
        checklist=questions,
        title='Контрольный лист посещения'
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
    for key in request.form:
        data[key] = request.form[key]
    database.save_checklist(object_num, selected_date, data)
    model = QListViewModel()
    model.num = data['uid']
    model.object_name = selected_obj.num + '-' + selected_obj.title
    return render_template(
        template,
        model=model,
        title='Список'
    )
