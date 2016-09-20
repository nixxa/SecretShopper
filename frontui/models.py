""" Data models """
from datetime import datetime
from frontui.linq import where


class ObjectInfo:
    """ Object info """
    def __init__(self, json_data=None):
        self.num = ''
        self.sort_num = 0
        self.type = ''
        self.title = ''
        self.address = ''
        self.with_cafe = False
        self.with_shop = False
        if json_data is not None:
            self.parse(json_data)
        return

    def parse(self, json_data):
        """ Parse JSON """
        self.num = json_data['object_num']
        try:
            self.sort_num = int(self.num)
        except:
            self.sort_num = -1
        self.type = json_data['object_type']
        self.title = json_data['object_title']
        self.address = json_data['object_address']
        self.with_cafe = json_data['with_cafe']
        self.with_shop = json_data['with_shop']
        return

    def __repr__(self):
        return '{{ num: {0}, type: {1} }}'.format(self.num, self.type)
    
    @staticmethod
    def from_json(json_data):
        """
        Parse JSON
        :type json_data: str
        :rtype: ObjectInfo
        """
        obj = ObjectInfo()
        obj.parse(json_data)
        return obj

    def applies(self, question):
        """
        Check that question applies to object
        :type question: QuestionInfo
        :rtype: bool
        """
        s = ''
        if self.with_shop:
            s = 'shop'
        if self.with_cafe:
            s = 'cafe'
        if s == '' and len(question.applies) == 0 and not self.num in question.excepts:
            return True
        if s == '' and len(question.applies) > 0 and self.num in question.applies:
            return True
        if s != '' and len(question.applies) == 0 and not self.num in question.excepts:
            return True
        return (s in question.applies or self.num in question.applies) and not self.num in question.excepts

class PageInfo:
    """ Page with questions """
    def __init__(self):
        self.title = ''
        self.num = 0
        self.cost = 0
        self.questions = list()

    def __repr__(self):
        return '{{ num: {0}, title: {1} }}'.format(self.num, self.title)

    @staticmethod
    def from_json(json_data):
        """ 
        Parse JSON 
        :type json_data: str
        :rtype: PageInfo
        """
        if json_data is None:
            return None
        page = PageInfo()
        page.title = json_data['title']
        page.num = int(json_data['num'])
        if 'cost' in json_data:
            page.cost = int(json_data['cost']) 
        for item in json_data['questions']:
            question = QuestionInfo.from_json(item)
            question.cost = page.cost
            if question is not None:
                page.questions.append(question)
        return page

    def max_cost(self, obj_info):
        """
        Return max points for PageInfo
        :type obj_info: ObjectInfo
        :rtype: int
        """
        applied = len(where(self.questions, lambda s: obj_info.applies(s)))
        excepts = 0 #len(where(self.questions, lambda s: obj_info.num in s.excepts))
        return self.cost * (applied - excepts)
        
    def max_questions(self, obj_info):
        """
        Return max questions count
        :type obj_info: ObjectInfo
        :rtype: int
        """
        applied = len(where(self.questions, lambda s: obj_info.applies(s)))
        excepts = 0 #len(where(self.questions, lambda s: obj_info.num in s.excepts))
        return applied - excepts


class QuestionInfo:
    """ Question """
    def __init__(self):
        self.label = ''
        self.field_name = ''
        self.cost = 0
        self.applies = []
        self.excepts = []
        self.optional = False

    def __repr__(self):
        return '{{ field: {0}, title: {1} }}'.format(self.field_name, self.label)

    @staticmethod
    def from_json(json_data):
        """
        Parse JSON
        :type json_data: str
        :rtype: QuestionInfo
        """
        if json_data is None:
            return None
        question = QuestionInfo()
        question.label = json_data['label']
        question.field_name = json_data['field_name']
        if 'applies' in json_data:
            question.applies = json_data['applies'].split(',')
        if 'excepts' in json_data:
            question.excepts = json_data['excepts'].split(',')
        if 'optional' in json_data:
            question.optional = True
        return question

class ChecklistInfo:
    """ Questionnaire data """
    def __init__(self):
        self.owner = ''
        self.pages = list()

    @staticmethod
    def from_json(json_data):
        """
        Parse JSON
        :type json_data: str
        :rtype: ChecklistInfo
        """
        if json_data is None:
            return None
        checklist = ChecklistInfo()
        checklist.owner = json_data['owner']
        for item in json_data['pages']:
            page = PageInfo.from_json(item)
            if page is not None:
                checklist.pages.append(page)
        return checklist


class Checklist:
    """ Filled checklist with data """
    def __init__(self, json_data=None):
        self.uid = None
        self.object_info = None
        self.checklist_info = None
        self.state = 'new'
        self.notice_sent = False
        self.create_date = datetime.utcnow()
        self.verify_date = None
        self.date = None
        self.files = list()
        self.visited_by = dict()
        if json_data is not None:
            self.__dict__.update(json_data)
            if 'create_date' in json_data:
                self.create_date = \
                    datetime.strptime(json_data['create_date'], '%Y-%m-%dT%H:%M:%S')
            if 'p1_r1' in json_data:
                self.date = \
                    datetime.strptime(json_data['p1_r1'],'%Y-%m-%d')
        self.max_points = 0
        self.points = 0
        self.points_percent = 0
        return

    def update(self, form_data):
        """
        Update field from dictionary object
        :type form_data: dict
        :rtype: None
        """
        if form_data is None:
            return
        if not isinstance(form_data, dict):
            return
        self.__dict__.update(form_data)
        return

    def get(self, field_name):
        """
        Return field value
        :type field_name: str
        """
        return self.__dict__[field_name] if field_name in self.__dict__ else None

    def sum_points(self, page):
        """
        Calculate sum of answered questions
        :type page: int
        :rtype: int
        """
        p = 0
        for q in page.questions:
            answer = self.get(q.field_name) == 'yes'
            if not self.object_info.applies(q):
                continue
            p = p + (page.cost if answer else 0)
        return p

    def visit_by(self, username):
        """
        Set checklist visited by user
        :type username: str
        """
        self.visited_by[username] = datetime.utcnow()
        return


class UserActionInfo:
    """ Defines user's information (actions time, last login time) """

    def __init__(self, json_data=None):
        self.username = None
        self.last_login_time = datetime(2000, 1, 1)
        self.last_edit_time = datetime(2000, 1, 1)
        if (json_data is not None):
            if 'username' in json_data:
                self.username = json_data['username']
            if 'last_login_time' in json_data and json_data['last_login_time'] is not None:
                self.last_login_time = datetime.strptime(json_data['last_login_time'], '%Y-%m-%dT%H:%M:%S')
            if 'last_login_time' in json_data and json_data['last_login_time'] is not None:
                self.last_login_time = datetime.strptime(json_data['last_login_time'], '%Y-%m-%dT%H:%M:%S')
        return

    def update_login_time(self):
        """ Update last login time, shift last to prev """
        self.last_login_time = datetime.utcnow()
        return

    def update_edit_time(self):
        """ Update last edit time, shift last to prev """
        self.last_edit_time = datetime.utcnow()
        return
