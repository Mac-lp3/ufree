import os
import unittest
import builtins
from classes.util.AttendeeValidator import AttendeeValidator
from classes.exception.ValidationException import ValidationException


class AvailabilityDaoTest(unittest.TestCase):

    def setUp (self):
        self.__validator = AttendeeValidator()

    def validate_attendee_request_test (self):
        pass

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
