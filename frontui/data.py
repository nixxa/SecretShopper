""" Data layer """
# pylint: disable=line-too-long
import json
import os
from frontui.models import ChecklistInfo


class DataProvider:
    """ Data provider (objects, questions, etc) """
    def __init__(self):
        self.data_dir = './frontui/app_data'
        self.checklists_dir = self.data_dir + '/checklists'
        self.objects = list()
        self.checklist = ChecklistInfo()


    def add_object(self, obj):
        """ Add object to collection """
        self.objects.append(obj)


    def save_checklist(self, obj_num, obj_date, obj_dict):
        """ Save checklist data """
        obj_json = json.dumps(obj_dict, sort_keys=True, indent=4)
        filedir = self.checklists_dir + '/' + obj_num
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filename = obj_date + '.json'
        with open(filedir + '/' + filename, 'w', encoding='utf8') as file:
            file.write(obj_json)
        return
