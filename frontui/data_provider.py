""" Data layer """
# pylint: disable=line-too-long
import json
import os
from frontui.models import ObjectInfo, ChecklistInfo


class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class DataProvider(Singleton):
    """ Data provider (objects, questions, etc) """

    def __init__(self):
        self.objects = list()
        self.checklist = ChecklistInfo()
        self.data_dir = './frontui/app_data'
        self.checklists_dir = self.data_dir + '/checklists'
        # fill data from files
        with open('./frontui/app_data/objects.json', 'r', encoding='utf8') as objects_file:
            for item in json.load(objects_file):
                self.add_object(ObjectInfo(item))
        with open('./frontui/app_data/checklist.json', 'r', encoding='utf8') as checklist_file:
            self.checklist = ChecklistInfo.from_json(json.load(checklist_file))

    def add_object(self, obj):
        """ Add object to collection """
        self.objects.append(obj)

    def save_checklist(self, obj_num, obj_date, obj_dict):
        """ Save checklist data """
        obj_json = json.dumps(obj_dict, sort_keys=True, indent=4, ensure_ascii=False)
        filedir = self.checklists_dir + '/' + obj_num
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filename = obj_date + '.json'
        with open(filedir + '/' + filename, 'w', encoding='utf8') as file:
            file.write(obj_json)
        return
