import os
import classes.exception.DaoException as DaoException
from classes.HashCodeUtils import HashCodeUtils

class EventDao:

    mock_event_ids = [
        'qwe1fd23qwe123qwe123qwe123asd345',
        '12345567890asdfghjklqwertyuiopzx'
    ]

    def event_exists (eventId):
        if eventId in EventDao.mock_event_ids:
            return True
        else:
            return False

    def load_event (eventId):
        if eventId in EventDao.mock_event_ids:
            return {
                'id': eventId,
                'name': 'A mock event',
                'creator': 'Tony T'
            }
        else:
            raise DaoException('Event wasn\'t in there')

    def save_event(eventObject):
        generatedId = HashCodeUtils.generate_code(eventObject['name'])
        EventDao.mock_event_ids.push(generatedId)
        return load_event(generatedId)

    def update_event(eventObject):
        return load_event(eventObject['id'])

    def delete_event(eventObject):
        if eventObject['id'] in EventDao.mock_event_ids:
            EventDao.mock_event_ids.remove(eventObject['id'])
        else:
            raise DaoException('Event wasn\'t in there')
