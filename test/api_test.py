import os
import json
import unittest
import builtins
import views.api as api
from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest
from test.classes.MockRequest import MockRequest

class ApiTest(unittest.TestCase):

    # test event ids
    __short_id = '123123123123123'
    __long_id = '123123123123123adsasdasdasdasj12jkas'
    __non_exist_id = 'asd234fgh234asd123dfg123dfg23dfg'
    __bad_char_id = 'sdkjhdsfakjh3232ksjdn$sdlk1dsw12'
    __good_id = 'qwe1fd23qwe123qwe123qwe123asd345'

    # test event names
    __bad_name = ') DROP TABLE \'USERS\''
    __good_name = 'A good name for the event'

    # test creator names
    __bad_creator = ') DROP TABLE \'USERS\''
    __good_creator = 'Tommy T'

    def post_event_fail_test (self):
        #test bad event name
        builtins.db_fail = 'False'
        post_body = {
            'name': self.__bad_name,
            'creator': self.__good_creator
        }
        req = MockRequest(body=post_body)
        resp = api.post_event(req)
        self.assertEqual(type(resp), HTTPBadRequest)
        e_list = resp.json_body['errors']
        print(resp.json_body)
        self.assertTrue(
            'Name must only contain letters, numbers, spaces, or dashes' in e_list
        )

        #test bad creator
        post_body = {
            'name': self.__good_name,
            'creator': self.__bad_creator
        }
        req = MockRequest(body=post_body)
        resp = api.post_event(req)
        self.assertEqual(type(resp), HTTPBadRequest)
        e_list = resp.json_body['errors']
        self.assertTrue(
            'Creator must only contain letters, numbers, spaces, or dashes' in e_list
        )

        # test DB exception
        builtins.db_fail = 'True'
        post_body = {
            'name': self.__good_name,
            'creator': self.__good_creator
        }
        req = MockRequest(body=post_body)
        try:
            resp = api.post_event(req)
        except Exception as e:
            self.assertEqual(type(e), HTTPBadRequest)
            self.assertEqual(
                'An error occurred while saving this event.', str(e)
            )
        builtins.db_fail = 'False'

    def post_event_success_test (self):
        builtins.db_fail = 'False'
        post_body = {
            'name': self.__good_name,
            'creator': self.__good_creator
        }
        req = MockRequest(body=post_body)
        resp = api.post_event(req)
        jbod = json.loads(resp.json_body)
        print('the resp', resp)
        print('resp json bod', jbod)
        self.assertNotEqual(type(resp), HTTPBadRequest)
        self.assertEqual(jbod['name'], 'A mock event')
        self.assertEqual(jbod['creator_id'], 'heyheyhey')

    def get_event_fail_test (self):
        # test bad id - too short
        req = MockRequest(self.__short_id)
        resp = api.get_event(req)
        e_list = resp.json_body['errors']
        self.assertEqual(type(resp), HTTPBadRequest)
        self.assertTrue('Hash is less than 32 characters' in e_list)

        # test bad id - too long
        req = MockRequest(self.__long_id)
        resp = api.get_event(req)
        e_list = resp.json_body['errors']
        self.assertEqual(type(resp), HTTPBadRequest)
        self.assertTrue('Hash is greater than 32 characters' in e_list)

        # test bad id - incorrect characters
        req = MockRequest(self.__bad_char_id)
        resp = api.get_event(req)
        e_list = resp.json_body['errors']
        self.assertEqual(type(resp), HTTPBadRequest)
        self.assertTrue('Hash can only include numbers and letters' in e_list)

        # test bad id - incorrect characters
        req = MockRequest(self.__non_exist_id)
        resp = api.get_event(req)
        e_list = resp.json_body['errors']
        print(e_list)
        self.assertEqual(type(resp), HTTPBadRequest)
        self.assertTrue(
            'Event wasn\'t in there' in e_list
        )

    def get_event_success_test (self):
        # test bad id - too short
        builtins.db_fail = 'False'
        req = MockRequest(self.__good_id)
        resp = api.get_event(req)
        jbod = json.loads(resp.json_body)
        self.assertNotEqual(resp, HTTPBadRequest)
        self.assertEqual(self.__good_id, jbod['id'])

if __name__ == '__main__':
	unittest.main()
