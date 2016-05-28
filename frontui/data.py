""" Data layer """
from frontui.models import ObjectInfo, ChecklistInfo


class DataProvider:
    """ Data provider (objects, questions, etc) """
    def __init__(self):
        self.objects = list()
        self.checklist = ChecklistInfo()


    def add_object(self, obj):
        """ Add object to collection """
        self.objects.append(obj)
