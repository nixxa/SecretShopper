""" Data models """


class ObjectInfo:
    """ Object info """
    def __init__(self, json_data=None):
        self.num = ''
        self.type = ''
        self.title = ''
        self.address = ''
        if json_data is not None:
            self.parse(json_data)

    def parse(self, json_data):
        """ Parse JSON """
        self.num = json_data['object_num']
        self.type = json_data['object_type']
        self.title = json_data['object_title']
        self.address = json_data['object_address']

    @staticmethod
    def from_json(json_data):
        """ Parse JSON """
        obj = ObjectInfo()
        obj.parse(json_data)
        return obj


class PageInfo:
    """ Page with questions """
    def __init__(self):
        self.title = ''
        self.num = 0
        self.questions = list()

    @staticmethod
    def from_json(json_data):
        """ Parse JSON """
        if json_data is None:
            return None
        page = PageInfo()
        page.title = json_data['title']
        page.num = int(json_data['num'])
        for item in json_data['questions']:
            question = QuestionInfo.from_json(item)
            if question is not None:
                page.questions.append(question)
        return page

class QuestionInfo:
    """ Question """
    def __init__(self):
        self.label = ''
        self.field_name = ''

    @staticmethod
    def from_json(json_data):
        """ Parse JSON """
        if json_data is None:
            return None
        question = QuestionInfo()
        question.label = json_data['label']
        question.field_name = json_data['field_name']
        return question

class ChecklistInfo:
    """ Questionnaire data """
    def __init__(self):
        self.owner = ''
        self.pages = list()

    @staticmethod
    def from_json(json_data):
        """ Parse JSON """
        if json_data is None:
            return None
        checklist = ChecklistInfo()
        checklist.owner = json_data['owner']
        for item in json_data['pages']:
            page = PageInfo.from_json(item)
            if page is not None:
                checklist.pages.append(page)
        return checklist
