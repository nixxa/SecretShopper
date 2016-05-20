"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask.ext.mobility.decorators import mobile_template
from flask.ext.mobility import Mobility
from frontui import app


Mobility(app)

@app.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/qlist')
@app.route('/qlist/')
@mobile_template('{mobile/}questionnaire.html')
def questionnaire(template):
    """Renders questionnaire page"""
    return render_template(
        template,
        title='Контрольный лист посещения'
    )
