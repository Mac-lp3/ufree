import os
import json
import unittest
from classes.util.event_validator import EventValidator

class EventValidatorTest(unittest.TestCase):

    def setUp(self):
        self.__goodEvent = {
            'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
            'name': 'This is a good name',
            'creator': 'Mikey Big C'
        }

        self.__starNameEvent = {
            'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
            'name': '* This is a bad name',
            'creator': 'Mikey Big C'
        }

        self.__closeNameEvent = {
            'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
            'name': ') This is a bad name',
            'creator': 'Mikey Big C'
        }

        self.__starCreatorEvent = {
            'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
            'name': 'This is a good name',
            'creator': 'Mikey Big * C'
        }

        self.__closeCreatorEvent = {
            'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
            'name': 'This is a good name',
            'creator': ') Mikey Big C'
        }

        self.__inputValidator = EventValidator()

    def test_event_fail_validation (self):
        try:
            test_messages = self.__inputValidator.validate_event(self.__starNameEvent)
        except Exception as e:
            payload = e.get_payload()
            jsonPayload = json.loads(payload)
            self.assertEqual(len(jsonPayload['errors']), 1)

        try:
            test_messages = self.__inputValidator.validate_event(self.__closeNameEvent)
        except Exception as e:
            payload = e.get_payload()
            jsonPayload = json.loads(payload)
            self.assertEqual(len(jsonPayload['errors']), 1)

        try:
            test_messages = self.__inputValidator.validate_event(self.__starCreatorEvent)
        except Exception as e:
            payload = e.get_payload()
            jsonPayload = json.loads(payload)
            self.assertEqual(len(jsonPayload['errors']), 1)

        try:
            test_messages = self.__inputValidator.validate_event(self.__closeCreatorEvent)
        except Exception as e:
            payload = e.get_payload()
            jsonPayload = json.loads(payload)
            self.assertEqual(len(jsonPayload['errors']), 1)

    def test_event_pass_validation (self):
        test_messages = self.__inputValidator.validate_event(self.__goodEvent)
        self.assertEqual(test_messages, None)

if __name__ == '__main__':
	unittest.main()
