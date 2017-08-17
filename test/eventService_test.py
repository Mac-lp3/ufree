import os
import json
import unittest
import hashlib
import builtins
from test.classes.MockRequest import MockRequest
from classes.service.EventService import EventService
from classes.exception.ServiceException import ServiceException
import test.classes.Const as const

# dir_path = os.path.dirname(os.path.realpath(__file__))
# fts = os.path.join(dir_path, '..\classes\util\HashCodeUtils.py')
# exec(open(fts).read())

class EventServiceTest(unittest.TestCase):

    __event_service = EventService()

    def load_event_test (self):
        ret = self.__event_service.load_event(MockRequest(
            id=const.GOOD_EVENT_ID
        ))
        print(ret)
        self.assertTrue('name' in ret)
        self.assertTrue('id' in ret)

        try:
            self.__event_service.load_event('123123')
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def update_event_test (self):
        post_body = {
            'id': const.GOOD_EVENT_ID,
            'name': 'idk some event',
            'creator': 'timmy t i guess'
        }
        req = MockRequest(body=post_body)
        ret = self.__event_service.update_event(req)
        print(ret)
        self.assertTrue('name' in ret)
        self.assertTrue('id' in ret)

        try:
            ret = self.__event_service.update_event({
                'name-o': 'idk some event',
                'creatGuy': 'timmy t i guess'
            })
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def create_event_test (self):
        post_body = {
            'id': const.GOOD_EVENT_ID,
            'name': 'idk some event',
            'creator': 'timmy t i guess'
        }
        req = MockRequest(body=post_body)
        ret = self.__event_service.create_event(req)
        print(ret)
        self.assertTrue('name' in ret)
        self.assertTrue('id' in ret)

        try:
            ret = self.__event_service.create_event({
                'name-o': 'idk some event',
                'creatGuy': 'timmy t i guess'
            })
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def delete_event_test(self):
        # creator should be able to delete their events
        try:
            self.__event_service.delete_event(MockRequest(
                id=const.GOOD_EVENT_ID
            ))
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)

        # only creator should be able to to delete
        try:
            self.__event_service.delete_event(MockRequest(
                id=const.GOOD_EVENT_ID,
                cookies={
                    'user_id': 'nonono'
                }
            ))
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def add_event_attendee_test (self):
        try:
            self.__event_service.add_event_attendee(MockRequest(
                    id=const.GOOD_EVENT_ID,
                    body={
                        'name': 'juan'
                    })
                )
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)

    def update_attendee_test (self):
        try:
            r = self.__event_service.update_event_attendee(MockRequest(
                    body={
                        'name': 'juan'
                    })
                )
            self.assertTrue(False)
        except Exception as e:
            print(e)
            self.assertEqual(str(e), 'Id was not found on this request')
            self.assertTrue(True)

        try:
            r = self.__event_service.update_event_attendee(MockRequest(
                    body={
                        'id': 'idklol',
                        'name': 'juan'
                    })
                )
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)

    def delete_event_attendee_test (self):
        # test normal behavior
        try:
            r = self.__event_service.delete_event_attendee(MockRequest(
                body={
                    'name': 'juan'
                },
                attendee_id=const.GOOD_USER_ID,
                    id=const.GOOD_EVENT_ID)
                )
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)

        # try to delete as another user
        try:
            r = self.__event_service.delete_event_attendee(MockRequest(
                body={
                    'name': 'juan'
                },
                attendee_id=const.GOOD_USER_ID,
                cookies={
                    'user_id': const.BAD_USER_ID
                })
            )
            print(r)
            self.assertTrue(False)
        except Exception as e:
            print(e)
            self.assertEqual(
                str(e),
                'Only the creator can remove other users from an event'
            )
            self.assertTrue(True)

    def get_event_attendees_test (self):
        # test regular behavior
        builtins.db_fail = 'False'
        res = self.__event_service.get_event_attendees(MockRequest(
            body={'event_id'}
        ))
        obj = json.loads(res)
        print(obj)
        self.assertEqual(len(obj), 2)

        # test error handling
        builtins.db_fail = 'True'
        try:
            res = self.__event_service.get_event_attendees(MockRequest(
                body={'event_id'}
            ))
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(type(e) is ServiceException)
            pass

    def update_attendee_availability_test (self):
        pass

if __name__ == '__main__':
    unittest.main()
