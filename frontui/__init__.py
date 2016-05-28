"""
The flask application package.
"""
#import logging
#import json
#import os
from flask import Flask
from frontui.data import DataProvider
#from frontui.models import ObjectInfo, ChecklistInfo
# create an application
app = Flask(__name__)
# set prod logging
#MODE = os.environ.get('APP_MODE', 'DEBUG')
#if MODE == 'PROD':
#    logging.basicConfig(filename='app.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
#    logging.debug('Starting app in %s mode' % MODE)
#else:
#    app.debug_log_format = '%(asctime)s %(levelname)s %(message)s'
#    app.logger.setLevel(logging.DEBUG)
# create data provider
DATA = DataProvider()
# fill data from files
#with open('./app_data/objects.json', 'r') as objects_file:
#    for item in json.load(objects_file):
#        DATA.add_object(ObjectInfo(item))
#with open('./app_data/checklist.json', 'r') as checklist_file:
#    DATA.checklist = ChecklistInfo.from_json(json.load(checklist_file))

import frontui.views
