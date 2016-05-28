"""
The flask application package.
"""
import logging
import json
from flask import Flask
from frontui.data import DataProvider
from frontui.models import ObjectInfo, ChecklistInfo
# create an application
app = Flask(__name__)
# set prod logging
app.debug_log_format = '%(asctime)s %(levelname)s %(message)s'
app.logger.setLevel(logging.DEBUG)
# create data provider
DATA = DataProvider()
# fill data from files
with open('./frontui/app_data/objects.json', 'r') as objects_file:
    for item in json.load(objects_file):
        DATA.add_object(ObjectInfo(item))
#with open('./app_data/checklist.json', 'r') as checklist_file:
#    DATA.checklist = ChecklistInfo.from_json(json.load(checklist_file))

import frontui.views
