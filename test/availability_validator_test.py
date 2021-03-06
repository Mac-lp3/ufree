import os
import json
import unittest
import test.classes.const as const
from test.classes.mock_request import MockRequest
from classes.util.availability_validator import AvailabilityValidator
from classes.exception.validation_exception import ValidationException

class AvailabilityValidatorTest(unittest.TestCase):

    def setUp (self):
        self.__validator = AvailabilityValidator()

        self.__good_year = '2017'
        self.__bad_year = '1997'

        self.__32_days = '00000000000000000000000000000000'
        self.__31_days = '0000000000000000000000000000000'
        self.__30_days = '000000000000000000000000000000'
        self.__28_days = '0000000000000000000000000000'

        self.__good_availability = {
            'id': '3425asdf',
            'attendee_id': 'asdf1234',
            'event_id': const.GOOD_EVENT_ID,
            'year': self.__good_year,
            'january': self.__31_days,
            'february': self.__28_days,
            'march': self.__31_days,
            'april': self.__30_days,
            'may': self.__31_days,
            'june': self.__30_days,
            'july': self.__31_days,
            'august': self.__31_days,
            'september': self.__30_days,
            'october': self.__31_days,
            'november': self.__30_days,
            'december': self.__31_days
        }

        self.__bad_month_length_availability = {
            'id': '3425asdf',
            'attendee_id': 'asdf1234',
            'event_id': const.GOOD_EVENT_ID,
            'year': self.__good_year,
            'january': self.__30_days,
            'february': self.__30_days,
            'march': self.__30_days,
            'april': self.__31_days,
            'may': self.__30_days,
            'june': self.__28_days,
            'july': self.__28_days,
            'august': self.__30_days,
            'september': self.__31_days,
            'october': self.__30_days,
            'november': self.__31_days,
            'december': self.__30_days
        }

        self.__bad_year_availability = {
            'id': '3425asdf',
            'attendee_id': 'asdf1234',
            'event_id': const.GOOD_EVENT_ID,
            'year': self.__bad_year,
            'january': self.__31_days,
            'february': self.__28_days,
            'march': self.__31_days,
            'april': self.__30_days,
            'may': self.__31_days,
            'june': self.__30_days,
            'july': self.__31_days,
            'august': self.__31_days,
            'september': self.__30_days,
            'october': self.__31_days,
            'november': self.__30_days,
            'december': self.__31_days
        }

    def validate_attendee_id_test (self):
        # validate a good id value
        try:
            self.__validator.validate_availability_id('abcd1234')
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)

        # validate a bad id value
        try:
            self.__validator.validate_availability_id(') * DROP TABLE USERS')
            self.assertTrue(False)
        except Exception as e:
            print(e)
            self.assertTrue(isinstance(e, ValidationException))

        # validate empty id
        try:
            self.__validator.validate_availability_id('')
            self.assertTrue(False)
        except Exception as e:
            print(e)
            self.assertTrue(isinstance(e, ValidationException))

    def vaildaite_availability_request_test (self):
        # validate a good availability object
        try:
            self.__validator.validate_availability_request(
                MockRequest(
                    body=self.__good_availability,
                    availability_id='1234ljh',
                    method='POST'
                )
            )
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)

        # validate an availability object with bad month lengths
        try:
            self.__validator.validate_availability_request(
                MockRequest(
                    body=self.__bad_month_length_availability,
                    availability_id='1234ljh',
                    method='POST'
                )
            )
            self.assertTrue(False)
        except Exception as e:
            print(e)
            self.assertTrue(isinstance(e, ValidationException))

        # validate an availability object with a bad year
        try:
            self.__validator.validate_availability_request(
                MockRequest(
                    body=self.__bad_year_availability,
                    availability_id='1234ljh',
                    method='POST'
                )
            )
            self.assertTrue(False)
        except Exception as e:
            print(e)
            self.assertTrue(isinstance(e, ValidationException))
