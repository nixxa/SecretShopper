""" Data layer """
# pylint: disable=line-too-long
import json
import os
import datetime
import logging
import shutil
import frontui.linq as linq
from frontui import BASE_DIR
from frontui.models import ObjectInfo, ChecklistInfo, Checklist, UserActionInfo, User

VISITS_FILENAME = 'app_data/user_visits.json'
OBJECTS_FILENAME = 'app_data/objects.json'
CHECKLIST_FILENAME = 'app_data/checklist.json'
USERS_FILENAME = 'app_data/users.json'
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')

logger = logging.getLogger(__name__)

class DateTimeAwareEncoder(json.JSONEncoder):
    """
    Datetime encoder
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        if isinstance(obj, UserActionInfo):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class DataProvider:
    """ Data provider (objects, questions, etc) """

    def __init__(self):
        self.objects = list()
        self.checklist = ChecklistInfo()
        self.checklists = list()
        self.data_dir = os.path.join(BASE_DIR, 'app_data')
        self.checklists_dir = os.path.join(self.data_dir, 'checklists')
        self.user_visits = dict()
        self.users = list()
        # fill data from files
        # load objects
        with open(os.path.join(BASE_DIR, OBJECTS_FILENAME), 'r', encoding='utf8') as objects_file:
            for item in json.load(objects_file):
                self.add_object(ObjectInfo(item))
        # load checklist info
        with open(os.path.join(BASE_DIR, CHECKLIST_FILENAME), 'r', encoding='utf8') as checklist_file:
            self.checklist = ChecklistInfo.from_json(json.load(checklist_file))
        # load filled checklists
        json_data = dict()
        for (dirpath, dirnames, filenames) in os.walk(self.checklists_dir):
            for fname in filenames:
                if os.path.splitext(fname)[1] != '.json':
                    continue
                with open(os.path.join(dirpath, fname), 'r', encoding='utf8') as file:
                    json_data = json.load(file)
                item = Checklist(json_data)
                if not hasattr(item, 'files'):
                    item.files = list()
                obj_info = linq.first_or_default(self.objects, lambda x: x.num == json_data['object_name'])
                item.object_info = obj_info
                item.checklist_info = self.checklist
                if not hasattr(item, 'notice_sent'):
                    item.notice_sent = False
                if not hasattr(item, 'state'):
                    item.state = 'new'
                self.checklists.append(item)
        # load user's visits
        if os.path.exists(os.path.join(BASE_DIR, VISITS_FILENAME)):
            with open(os.path.join(BASE_DIR, VISITS_FILENAME), 'r', encoding='utf8') as visits_file:
                json_data = json.load(visits_file)
                for key in json_data:
                    self.user_visits[key] = UserActionInfo(json_data[key])
        # load users
        if os.path.exists(os.path.join(BASE_DIR, USERS_FILENAME)):
            with open(os.path.join(BASE_DIR, USERS_FILENAME), 'r', encoding='utf8') as users_file:
                json_data = json.load(users_file)
                for user_data in json_data:
                    self.users.append(User(user_data))
        return


    def get_uploads_dir(self, checklist):
        """
        Return folder for uploads
        """
        filedir = os.path.join(
            UPLOADS_DIR,
            checklist.date.strftime('%Y'),
            checklist.date.strftime('%m'),
            checklist.object_info.num,
            checklist.uid)
        return filedir


    def add_object(self, obj):
        """ Add object to collection """
        self.objects.append(obj)
        return


    def save_checklist(self, obj_num, obj_date, obj_dict):
        """ Save checklist data """
        obj_json = json.dumps(obj_dict, sort_keys=True, indent=4, ensure_ascii=False, cls=DateTimeAwareEncoder)
        filedir = os.path.join(self.checklists_dir, obj_num)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filename = obj_date + '.json'
        with open(os.path.join(filedir, filename), 'w', encoding='utf8') as file:
            file.write(obj_json)
        return


    def update_checklist(self, obj):
        """
        Update checklist
        :rtype: None
        """
        obj_num = obj.object_info.num
        obj_date = obj.date.strftime('%Y-%m-%d')
        obj_dict = obj.__dict__.copy()
        del obj_dict['object_info']
        del obj_dict['checklist_info']
        obj_json = json.dumps(obj_dict, sort_keys=True, indent=4, ensure_ascii=False, cls=DateTimeAwareEncoder)
        filedir = os.path.join(self.checklists_dir, obj_num)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filename = obj_date + '.json'
        with open(os.path.join(filedir, filename), 'w', encoding='utf8') as file:
            file.write(obj_json)
        return


    def remove_checklist(self, checklist=None, uid=None):
        """
        Remove checklist
        """
        if checklist is None and uid is None:
            return
        if uid is not None:
            checklist = linq.first_or_default(self.checklists, lambda x: x.uid == uid)
        if checklist is None:
            return
        # rename checklist file
        logger.info('Removing checklist: %s', checklist.uid)
        filedir = os.path.join(self.checklists_dir, checklist.object_info.num)
        filename = checklist.date.strftime('%Y-%m-%d') + '.json'
        backup_filename = checklist.date.strftime('%Y-%m-%d') + '.json.bak'
        shutil.move(os.path.join(filedir, filename), os.path.join(filedir, backup_filename))
        # rename uploads
        logger.info('Removing checklist uploads: %s', checklist.uid)
        uploads_dir = self.get_uploads_dir(checklist)
        backup_uploads_dir = uploads_dir + '.bak'
        try:
            shutil.move(uploads_dir, backup_uploads_dir)
        except Exception as ex:
            logger.exception('Cant remove uploads dir: %s', ex)
        return


    def get_user_action(self, username):
        """
        :rtype: UserActionInfo
        """
        if username not in self.user_visits:
            logger.debug('Create new UserActionInfo for %s', username)
            obj = UserActionInfo()
            obj.username = username
            obj.last_edit_time = datetime.datetime(2000, 1, 1)
            obj.prev_edit_time = datetime.datetime(2000, 1, 1)
            obj.last_login_time = datetime.datetime(2000, 1, 1)
            obj.prev_login_time = datetime.datetime(2000, 1, 1)
            self.user_visits[username] = obj
            return obj
        return self.user_visits[username]


    def save_user_actions(self):
        """
        Update user action and save to disk
        :rtype: None
        """
        obj_json = json.dumps(self.user_visits, sort_keys=True, indent=4, ensure_ascii=False, cls=DateTimeAwareEncoder)
        with open(os.path.join(BASE_DIR, VISITS_FILENAME), 'w', encoding='utf8') as file:
            file.write(obj_json)
        return
