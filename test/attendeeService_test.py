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
        # test correct usage
        req = MockRequest(event_id=const.GOOD_EVENT_ID)
        ret = self.__attendee_service.load_event_attendees(req)
        data = json.loads(ret.json_body)
        self.assertEqual(len(data), 2)
        self.assertTrue('name' in data[0])
        self.assertTrue('id' in data[0])
        self.assertTrue('name' in data[1])
        self.assertTrue('id' in data[1])

        # test bad event id
        try:
            req = MockRequest(event_id='dasfasdfasdasf')
            ret = self.__attendee_service.load_event_attendees(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

        # test db exception
        builtins.db_fail = True
        try:
            req = MockRequest(event_id=const.GOOD_EVENT_ID)
            self.__attendee_service.load_event_attendees(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def load_attendee_test (self):
        # test correct usage
        req = MockRequest(attendee_id=const.GOOD_USER_ID)
        ret = self.__attendee_service.load_attendee(req)
        data = json.loads(ret.json_body)
        self.assertEqual(len(data), 3)
        self.assertTrue('name' in data)
        self.assertTrue('id' in data)
        self.assertTrue('email' in data)

        # test bad event id
        try:
            req = MockRequest(attendee_id='()*^@#^)')
            ret = self.__attendee_service.load_attendee(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

        # test db exception
        builtins.db_fail = True
        try:
            req = MockRequest(attendee_id=const.GOOD_USER_ID)
            self.__attendee_service.load_attendee(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def update_attendee_test (self):
        # test good field names
        post_body = {
            'id': const.GOOD_USER_ID,
            'name': 'New Name'
        }
        req = MockRequest(body=post_body)
        ret = self.__attendee_service.update_attendee(req)
        self.assertTrue('name' in ret.json_body)
        self.assertTrue('id' in ret.json_body)

        # test bad request names
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
