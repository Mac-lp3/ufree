import os
import unittest
from classes.ApiInputValidator import ApiInputValidator

class ApiInputValidatorTest(unittest.TestCase):

    __goodEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': 'This is a good name',
        'creator': 'Mikey Big C'
    }

    __starNameEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': '* This is a bad name',
        'creator': 'Mikey Big C'
    }

    __closeNameEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': ') This is a bad name',
        'creator': 'Mikey Big C'
    }

    __starCreatorEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': 'This is a good name',
        'creator': 'Mikey Big * C'
    }

    __closeCreatorEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': 'This is a good name',
        'creator': ') Mikey Big C'
    }

    __inputValidator = ApiInputValidator()

    def test_event_fail_validation (self):
        test_messages = self.__inputValidator.validate_event(self.__starNameEvent)
        self.assertEqual(len(test_messages), 1)

        test_messages = self.__inputValidator.validate_event(self.__closeNameEvent)
        self.assertEqual(len(test_messages), 1)

        test_messages = self.__inputValidator.validate_event(self.__starCreatorEvent)
        self.assertEqual(len(test_messages), 1)

        test_messages = self.__inputValidator.validate_event(self.__closeCreatorEvent)
        self.assertEqual(len(test_messages), 1)

    def test_event_pass_validation (self):
        test_messages = self.__inputValidator.validate_event(self.__goodEvent)
        print(test_messages)
        self.assertEqual(len(test_messages), 0)

if __name__ == '__main__':
	unittest.main()
