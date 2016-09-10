""" Data layer """
# pylint: disable=line-too-long
import json
import os
import frontui.linq as linq
import datetime
from frontui.models import ObjectInfo, ChecklistInfo, Checklist
from flask import current_app


class DateTimeAwareEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        return json.JSONEncoder.default(self, obj)


class Singleton(object):
    """ Singleton superclass """
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
        self.checklists = list()
        self.data_dir = './frontui/app_data'
        self.checklists_dir = self.data_dir + '/checklists'
        # fill data from files
        # load objects
        with open('./frontui/app_data/objects.json', 'r', encoding='utf8') as objects_file:
            for item in json.load(objects_file):
                self.add_object(ObjectInfo(item))
        # load checklist info
        with open('./frontui/app_data/checklist.json', 'r', encoding='utf8') as checklist_file:
            self.checklist = ChecklistInfo.from_json(json.load(checklist_file))
        # load filled checklists
        json_data = dict()
        for (dirpath, dirnames, filenames) in os.walk(self.checklists_dir):
            for fname in filenames:
                if os.path.splitext(fname)[1] != '.json':
                    continue
                with open(dirpath + '/' + fname, 'r', encoding='utf8') as file:
                    json_data = json.load(file)
                item = Checklist(json_data)
                if not hasattr(item, 'files'):
                    item.files = list()
                obj_info = linq.first_or_default(self.objects, lambda x: x.num == json_data['object_name'])
                item.object_info = obj_info
                item.checklist_info = self.checklist
                if not hasattr(item, 'notice_sent'):
                    item.notice_sent = False        
                self.checklists.append(item)
        return


    def add_object(self, obj):
        """ Add object to collection """
        self.objects.append(obj)
        return


    def save_checklist(self, obj_num, obj_date, obj_dict):
        """ Save checklist data """
        obj_json = json.dumps(obj_dict, sort_keys=True, indent=4, ensure_ascii=False, cls=DateTimeAwareEncoder)
        filedir = self.checklists_dir + '/' + obj_num
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filename = obj_date + '.json'
        with open(filedir + '/' + filename, 'w', encoding='utf8') as file:
            file.write(obj_json)
        return


    def update_checklist(self, obj):
        """ Update checklist """
        obj_num = obj.object_info.num
        obj_date = obj.date.strftime('%Y-%m-%d')
        obj_dict = obj.__dict__.copy()
        del obj_dict['object_info']
        del obj_dict['checklist_info']
        obj_json = json.dumps(obj_dict, sort_keys=True, indent=4, ensure_ascii=False, cls=DateTimeAwareEncoder)
        filedir = self.checklists_dir + '/' + obj_num
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filename = obj_date + '.json'
        with open(filedir + '/' + filename, 'w', encoding='utf8') as file:
            file.write(obj_json)
        return
