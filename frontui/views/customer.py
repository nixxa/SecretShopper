""" Reports, administration """
#pylint: disable=line-too-long

import logging
import os
from datetime import datetime, timedelta
from flask import render_template, request, Blueprint, redirect, session, send_file
from frontui import BASE_DIR
from frontui.data_provider import DataProvider
from frontui.views.member import add_one_month, calculate_date_period, calc_points
from frontui.auth import authorize
from frontui.linq import first_or_default, where, count, select
from openpyxl import load_workbook

customer_ui = Blueprint('customer', __name__)
logger = logging.getLogger(__name__)


@customer_ui.route('/customer/reports', defaults={ 'date': None })
@customer_ui.route('/customer/reports/<date>')
@authorize
def customer_reports(date):
    """
    Render all verified reports by month
    """
    database = DataProvider()
    model = dict()
    #items = sorted(where(database.checklists, lambda x: x.state == 'verified'), key=lambda x: x.date)
    start_date = datetime.now().replace(day=1)
    if date is not None:
        start_date = datetime.strptime(date, '%Y%m%d')
    month_data = dict()
    month_data['date'] = start_date
    (shifted_start, shifted_end) = calculate_date_period(start_date)
    month_data['checklists'] = where(database.checklists, lambda x: x.date > shifted_start and x.date < shifted_end and x.state == 'verified')
    for rep in month_data['checklists']:
        calc_points(rep)
    model['month_data'] = month_data
    # build months list
    model['months'] = list()
    stop_date = datetime.strptime('20160801', '%Y%m%d')
    next_date = datetime.now().replace(day=1)
    while next_date >= stop_date:
        model['months'].append(next_date)
        next_date = next_date - timedelta(days=1)
        next_date = next_date.replace(day=1)
    # render template
    return render_template(
        'customer_reports.html',
        model=model,
        title='Отчеты по месяцам'
    )