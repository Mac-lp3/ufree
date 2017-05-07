import os
import unittest

dir_path = os.path.dirname(os.path.realpath(__file__))
fts = os.path.join(dir_path, '..\classes\ApiInputValidator.py')
exec(open(fts).read())

class ApiInputValidatorTest(unittest.TestCase):

    goodEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': 'This is a good name',
        'creator': 'Mikey Big C'
    }

    starNameEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': '* This is a bad name',
        'creator': 'Mikey Big C'
    }

    closeNameEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': ') This is a bad name',
        'creator': 'Mikey Big C'
    }

    starCreatorEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': 'This is a good name',
        'creator': 'Mikey Big * C'
    }

    closeCreatorEvent = {
        'id': 'kjhafu24kjsdncvhj23an3n32k1io213',
        'name': 'This is a good name',
        'creator': ') Mikey Big C'
    }

    def test_event_validation (self):
        test_messages = ApiInputValidator.validate_event(self.starNameEvent)
        self.assertEqual(len(test_messages), 1)

        test_messages = ApiInputValidator.validate_event(self.closeNameEvent)
        self.assertEqual(len(test_messages), 1)

        test_messages = ApiInputValidator.validate_event(self.starCreatorEvent)
        self.assertEqual(len(test_messages), 1)

        test_messages = ApiInputValidator.validate_event(self.closeCreatorEvent)
        self.assertEqual(len(test_messages), 1)

        test_messages = ApiInputValidator.validate_event(self.goodEvent)
        self.assertEqual(len(test_messages), 0)

if __name__ == '__main__':
	unittest.main()
