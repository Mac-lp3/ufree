import os
import json
import unittest
import hashlib
import builtins
import test.classes.Const as const
from test.classes.MockRequest import MockRequest
from classes.service.AttendeeService import AttendeeService
from classes.exception.ServiceException import ServiceException

class AttendeeServiceTest(unittest.TestCase):

    def setUp (self):
        builtins.db_fail = False
        self.__attendee_service = AttendeeService()

    def load_event_attendees_test (self):
        pass

    def load_attendee_test (self):
        pass

    def update_attendee_test (self):
        post_body = {
            'id': const.GOOD_USER_ID,
            'name': 'New Name'
        }
        req = MockRequest(body=post_body)
        ret = self.__attendee_service.update_attendee(req)
        print(ret)
        self.assertTrue('name' in ret.json_body)
        self.assertTrue('id' in ret.json_body)

        try:
            ret = self.__attendee_service.update_attendee({
                'name-o': 'idk some event',
                'creatGuy': 'timmy t i guess'
            })
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def update_attendee_availability_test (self):
        pass

    def get_event_attendees_test (self):
        pass

    def create_attendee_test (self):
        pass

    def remove_attendee_from_event_test (self):
        pass

    def add_attendee_to_event_test (self):
        pass
