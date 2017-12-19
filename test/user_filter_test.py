import os
import unittest
import hashlib
from test.classes.mock_request import MockRequest
from classes.filter.user_filter import UserFilter
from classes.exception.validation_exception import ValidationException

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
        try:
            req = MockRequest(body={'creator': 'Jimmy'})
            res = self.__filter.set_user_id(req)
            self.assertTrue(hasattr(res, 'cookies'))
            self.assertTrue(res.cookies['user_id'])
        except Exception as e:
            print('exception', str(e))
            self.assertTrue(False)

        # test no cookies w/ neither in body
        try:
            req = MockRequest()
            res = self.__filter.set_user_id(req)
            self.assertTrue(False, 'Should have thrown an exception')
        except Exception as e:
            print('exception', str(e))
            self.assertTrue(isinstance(e, ValidationException))
