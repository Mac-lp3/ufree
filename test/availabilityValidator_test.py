import os
import json
import unittest
import test.classes.Const as const
from test.classes.MockRequest import MockRequest
from classes.util.AvailabilityValidator import AvailabilityValidator

class AvailabilityValidatorTest(unittest.TestCase):

    def setUp (self):
        self.__validator = AvailabilityValidator()

        self.__good_year = 2017
        self.__bad_year = 1997

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

    def vaildaite_availability_request_test (self):
        try:
            self.__validator.validate_availability_request(
                MockRequest(
                    body=self.__good_availability,
                    availability_id='1234ljh',
                    method='POST'
                )
            )
        except Exception as e:
            print(e)
            self.assertTrue(False)
