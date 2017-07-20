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
        # test no cookies w/ creator in body
        # test no cookies w/ neither in body
        try:
            req = MockRequest(body={'name': 'Jimmy'})
            res = self.__filter.set_user_id(req)
            print(res)
        except Exception as e:
            print(e)
        print(UserFilter())
        self.assertTrue(False)
