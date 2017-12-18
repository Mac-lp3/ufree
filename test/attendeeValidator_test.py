import os
import unittest
import builtins
import test.classes.const as const
from test.classes.mock_request import MockRequest
from classes.util.attendee_validator import AttendeeValidator
from classes.exception.validation_exception import ValidationException


class AvailabilityDaoTest(unittest.TestCase):

    def setUp (self):
        self.__validator = AttendeeValidator()

    def validate_attendee_request_test (self):
        # test name not/in body
        # test id not/in body and not/in cookies

        # test normal behavior
        test_body = {
            'id': 'asdasd',
            'name': 'A fine name'
        }
        req = MockRequest(body=test_body)
        try:
            ers = self.__validator.validate_attendee_request(req)
            self.assertTrue(ers is None)
        except Exception as e:
            print(e)
            self.assertTrue(False)

        # test no name
        test_body = {
            'id': 'asdasd'
        }
        req = MockRequest(body=test_body)
        try:
            ers = self.__validator.validate_attendee_request(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ValidationException))

        # test no id in request
        test_body = {
            'name': 'A Good Name'
        }
        test_cookies = {
            'user_id': 'asdf234'
        }
        req = MockRequest(body=test_body, cookies=test_cookies)
        try:
            ers = self.__validator.validate_attendee_request(req)
            self.assertTrue(ers is None)
        except Exception as e:
            print(e)
            self.assertTrue(False)

        # test no id at all
        test_body = {
            'name': 'Some other name'
        }
        req = MockRequest(body=test_body, cookies={'idk why': 'lol'})
        try:
            ers = self.__validator.validate_attendee_request(req)
            self.assertTrue(False)
        except Exception as e:
            print(e)
            self.assertTrue(isinstance(e, ValidationException))

    def validate_attendee_name_test (self):
        # test type - bad
        try:
            self.__validator.validate_attendee_name(2345345)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ValidationException))

        # test type - good
        try:
            self.__validator.validate_attendee_name('robby ray')
        except Exception as e:
            print(e)
            self.assertTrue(False)

        # test length - bad
        try:
            self.__validator.validate_attendee_name(
                'asdfasdfasdfsdfasdfas12341243AB'
            )
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ValidationException))

        # test length - good
        try:
            self.__validator.validate_attendee_name(
                'asdfasdfasdfsdfasdfas12341243A'
            )
        except Exception as e:
            print(e)
            self.assertTrue(False)

        # test format - bad
        try:
            self.__validator.validate_attendee_name(') DELETE *')
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ValidationException))

        # test format - good
        try:
            self.__validator.validate_attendee_name('DELETE')
        except Exception as e:
            print(e)
            self.assertTrue(False)

    def validate_attendee_id_test (self):
        # test id - bad
        try:
            self.__validator.validate_attendee_name(') DELETE *')
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ValidationException))

        # test format - good
        try:
            self.__validator.validate_attendee_name('DELETE')
        except Exception as e:
            print(e)
            self.assertTrue(False)
