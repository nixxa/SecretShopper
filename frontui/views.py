"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from frontui import app

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
def questionnaire():
    """Renders questionnaire page"""
    return render_template(
        'questionnaire.html',
        title='Контрольный лист посещения'
    )
