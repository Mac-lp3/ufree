import os
from classes.exception.DaoException import DaoException
from classes.HashCodeUtils import HashCodeUtils

class EventDao:

    __mock_event_ids = [
        'qwe1fd23qwe123qwe123qwe123asd345',
        '12345567890asdfghjklqwertyuiopzx'
    ]

    def event_exists (eventId):
        print('Calling exists??')
        if eventId in EventDao.__mock_event_ids:
            return True
        else:
            return False

    def load_event (self, eventId):
        print('Calling load')
        if eventId in self.__mock_event_ids:
            print('id found in list')
            return {
                'id': eventId,
                'name': 'A mock event',
                'creator': 'Tony T'
            }
        else:
            print('id not found')
            raise DaoException('Event wasn\'t in there')

    def save_event(eventObject):
        print('Calling save')
        generatedId = HashCodeUtils.generate_code(eventObject['name'])
        EventDao.__mock_event_ids.push(generatedId)
        return load_event(generatedId)

    def update_event(eventObject):
        print('Calling update')
        return load_event(eventObject['id'])

    def delete_event(eventObject):
        print('Calling delete')
        if eventObject['id'] in EventDao.mock_event_ids:
            EventDao.mock_event_ids.remove(eventObject['id'])
        else:
            raise DaoException('Event wasn\'t in there')
