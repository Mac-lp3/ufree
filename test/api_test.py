import os
import unittest
from views.api import get_event
from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest

class ApiTest(unittest.TestCase):

    __short_id = '123123123123123'
    __long_id = '123123123123123adsasdasdasdasj12jkas'
    __bad_char_id = 'sdkjhdsfakjh3232ksjdn$sdlk1dsw12'
    __good_id = 'asd234fgh234asd123dfg123dfg23dfg'

    def get_event_fail_test (self):
        # test bad id - too short
        req = MockRequest(self.__short_id)
        resp = get_event(req)
        self.assertEqual(type(resp), HTTPBadRequest)

        # test bad id - too long
        req = MockRequest(self.__long_id)
        resp = get_event(req)
        self.assertEqual(type(resp), HTTPBadRequest)

        # test bad id - too incorrect characters
        req = MockRequest(self.__bad_char_id)
        resp = get_event(req)
        self.assertEqual(type(resp), HTTPBadRequest)

    def get_event_success_test (self):
        # test bad id - too short
        req = MockRequest(self.__good_id)
        resp = get_event(req)
        print('the resp', resp)
        self.assertEqual(1, HTTPBadRequest)

class MockRequest():

    matchdict = {}

    def __init__ (self, id):
        self.matchdict = {'eventId': id}

if __name__ == '__main__':
	unittest.main()
