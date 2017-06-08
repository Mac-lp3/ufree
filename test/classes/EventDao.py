import os
from classes.exception.DaoException import DaoException
from classes.util.HashCodeUtils import HashCodeUtils

class EventDao:

    __mock_event_ids = [
        'qwe1fd23qwe123qwe123qwe123asd345',
        '12345567890asdfghjklqwertyuiopzx'
    ]

    def event_exists (eventId):
        print('Calling exists??')
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        if eventId in EventDao.__mock_event_ids:
            return True
        else:
            return False

    def load_event (self, eventId):
        print('Calling load')
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        if eventId in self.__mock_event_ids:
            print('id found in list')
            return {
                'id': eventId,
                'name': 'A mock event',
                'creator_id': 'heyheyhey'
            }
        else:
            print('id not found')
            raise DaoException('Event wasn\'t in there')

    def save_event(self, eventObject):
        print('Calling save')
        if os.environ['TEST_DB_FAIL'] == 'True':
            raise DaoException('General exception')
        generatedId = HashCodeUtils.generate_code(eventObject['name'])
        self.__mock_event_ids.append(generatedId)
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
        if event_id not in self.__mock_event_ids:
            raise DaoException('Event wasn\'t in there')
