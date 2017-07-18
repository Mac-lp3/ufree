import os
import unittest
import hashlib
from classes.filter.UserFilter import UserFilter

class UserFilterTest(unittest.TestCase):

    def setUp (self):
        self.__filter = UserFilter()

    def set_user_id_test (self):
        # test no cookies w/ name in body
        # test no cookies w/ creator in body
        # test no cookies w/ neither in body
        pass
