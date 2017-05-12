import os
import json
import unittest
from views.api import get_event
from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest

class ApiTest(unittest.TestCase):

    __short_id = '123123123123123'
    __long_id = '123123123123123adsasdasdasdasj12jkas'
    __non_exist_id = 'asd234fgh234asd123dfg123dfg23dfg'
    __bad_char_id = 'sdkjhdsfakjh3232ksjdn$sdlk1dsw12'
    __good_id = 'qwe1fd23qwe123qwe123qwe123asd345'

    def get_event_fail_test (self):
        # test bad id - too short
        req = MockRequest(self.__short_id)
        resp = get_event(req)
        self.assertEqual(type(resp), HTTPBadRequest)
        self.assertTrue('Hash is less than 32 characters' in resp.json_body)

        # test bad id - too long
        req = MockRequest(self.__long_id)
        resp = get_event(req)
        self.assertEqual(type(resp), HTTPBadRequest)
        self.assertTrue('Hash is greater than 32 characters' in resp.json_body)

        # test bad id - incorrect characters
        req = MockRequest(self.__bad_char_id)
        resp = get_event(req)
        self.assertEqual(type(resp), HTTPBadRequest)
        self.assertTrue('Hash can only include numbers and letters' in resp.json_body)

        # test bad id - incorrect characters
        req = MockRequest(self.__non_exist_id)
        resp = get_event(req)
        self.assertEqual(type(resp), HTTPBadRequest)
        self.assertEqual(
            'An error occurred while loading this event.',
            resp.json_body['errors']
        )

    def get_event_success_test (self):
        # test bad id - too short
        req = MockRequest(self.__good_id)
        resp = get_event(req)
        jbod = json.loads(resp)
        self.assertNotEqual(resp, HTTPBadRequest)
        self.assertEqual(self.__good_id, jbod['id'])

class MockRequest():

    matchdict = {}

    def __init__ (self, id):
        self.matchdict = {'eventId': id}

if __name__ == '__main__':
	unittest.main()
