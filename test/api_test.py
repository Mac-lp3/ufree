import os
import unittest

dir_path = os.path.dirname(os.path.realpath(__file__))
fts = os.path.join(dir_path, '..\\views\\api.py')
exec(open(fts).read())

class ApiTest(unittest.TestCase):

    __short_id = '123123123123123'
    __long_id = '123123123123123adsasdasdasdasj12jkas'
    __bad_char_id = 'sdkjhdsfakjh3232ksjdn$sdlk1dsw12'

    def get_event_test (self):
        # test bad id - too short
        resp = get_event({'eventId': self.__short_id})
        self.assertEqual(type(resp), HTTPBadRequest)

        # test bad id - too long
        resp = get_event({'eventId': self.__long_id})
        self.assertEqual(type(resp), HTTPBadRequest)

        # test bad id - too incorrect characters
        resp = get_event({'eventId': self.__bad_char_id})
        self.assertEqual(type(resp), HTTPBadRequest)


if __name__ == '__main__':
	unittest.main()
