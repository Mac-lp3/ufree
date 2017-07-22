import os
import unittest
import hashlib
from test.classes.MockRequest import MockRequest
from classes.filter.UserFilter import UserFilter

class UserFilterTest(unittest.TestCase):

    def setUp (self):
        self.__filter = UserFilter()

    def set_user_id_test (self):
        # test no cookies w/ name in body
        try:
            req = MockRequest(body={'name': 'Jimmy'})
            res = self.__filter.set_user_id(req)
            self.assertTrue(hasattr(res, 'cookies'))
            self.assertTrue(res.cookies['user_id'])
        except Exception as e:
            print('exception', str(e))
            self.assertTrue(False)

        # test no cookies w/ creator in body
        # test no cookies w/ neither in body
