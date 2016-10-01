import unittest
from context import DataProvider


class TestUserActionInfo(unittest.TestCase):
    """ Test case """
    def test_save_user_action(self):
        database = DataProvider()
        action = database.get_user_action('anna')
        dt = action.last_login_time
        action.update_login_time()
        self.assertEqual(dt, action.prev_login_time)
        
        dt = action.last_login_time
        action.update_login_time()
        self.assertEqual(dt, action.prev_login_time)
        return

if __name__ == '__main__':
    unittest.main()