import os
import sys
import importlib
import builtins
from classes.exception.dao_exception import DaoException

class AttendeeDao:

    def leave_event (self, attendee_id, event_id):
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        print('leaving this event...')

    def save_attendee (self, attendee):
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        data = {
            'id': 'asd',
            'name': 'idkidkidk',
            'email': 'idk@lol.com'
        }
        return data

    def update_attendee (self, attendee):
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        data = {
            'id': 'asd',
            'name': 'idkidkidk',
            'email': 'idk@lol.com'
        }
        return data

    def load_attendee (self, attendee_id):
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        data = {
            'id': 'asd',
            'name': 'idkidkidk',
            'email': 'idk@lol.com'
        }
        return data

    def load_event_attendees (self, event_id):
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('test exception')
        data = [{
            'id': 'asd',
            'name': 'idkidkidk',
            'email': 'idk@lol.com'
            }, {
            'id': 'asd',
            'name': 'idkidkidk',
            'email': 'idk@lol.com'
        }]
        return data

    def attendee_exists (self, attendee_id):
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        return False

    def delete_attendee (self, attendee_id, event_id):
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        pass

    def join_event (self, attendee, event_id):
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        pass
