"""
Routes and views for the flask application.
"""
# pylint: disable=line-too-long

from datetime import datetime
from flask import render_template
from flask.ext.mobility.decorators import mobile_template
from flask.ext.mobility import Mobility
from frontui import APP as app, DATA
from frontui.view_models import QListViewModel


Mobility(app)

@app.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/checklist')
@mobile_template('{mobile/}checklist.html')
def questionnaire(template):
    """Renders questionnaire page"""
    objects = DATA.objects
    checklist = DATA.checklist
    return render_template(
        template,
        objects=objects,
        checklist=checklist,
        title='Контрольный лист посещения'
    )


@app.route('/save_list', methods=['POST'])
@mobile_template('{mobile/}checklist_saved.html')
def save(template):
    """ Save questionnaire and render success page """
    model = QListViewModel()
    model.num = '1234-5678'
    model.object_name = 'АЗС №5468'
    return render_template(
        template,
        model=model,
        title='Список'
    )
