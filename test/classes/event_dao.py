import os
from classes.exception.dao_exception import DaoException
from classes.util.hash_utils import HashCodeUtils
import test.classes.Const as const

class EventDao:

    def event_exists (eventId):
        print('Calling exists??')
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        if eventId in const.MOCK_EVENT_IDS:
            return True
        else:
            return False

    def load_event (self, eventId):
        print('Calling load')
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        if eventId in const.MOCK_EVENT_IDS:
            print('id found in list')
            return {
                'id': eventId,
                'name': 'A mock event',
                'creator_id': const.GOOD_USER_ID
            }
        else:
            print('id not found')
            raise DaoException('Event wasn\'t in there')

    def save_event(self, eventObject):
        print('Calling save')
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        generatedId = HashCodeUtils.generate_code(eventObject['name'])
        const.MOCK_EVENT_IDS.append(generatedId)
        return self.load_event(generatedId)

    def update_event(self, eventObject):
        print('Calling update')
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        return self.load_event(eventObject['id'])

    def delete_event(self, event_id):
        print('Calling delete')
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        if event_id not in const.MOCK_EVENT_IDS:
            raise DaoException('Event wasn\'t in there')
