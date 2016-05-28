""" View models definitions """
from datetime import datetime


class QListViewModel:
    """ Short definition of qlist general props """
    def __init__(self):
        """ c-tor """
        self.num = ''
        self.object_name = ''
        self.save_date = datetime.utcnow()
