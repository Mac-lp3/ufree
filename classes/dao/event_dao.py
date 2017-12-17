import os
import sys
import importlib
import datetime
from classes.dao.base_dao import BaseDao
from classes.exception.dao_exception import DaoException
from classes.util.HashCodeUtils import HashCodeUtils

class EventDao (BaseDao):

    def __init__ (self):
        BaseDao.__init__(self)

    def event_exists(self, eventId):
        try:
            self._cur.execute('SELECT name FROM event WHERE id = {0}'.format(eventId))
            val = self._cur.fetchone()
            return val is not None
        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException('Unknown error when searching for event')

    def load_event(self, eventId):
        '''
        Loads an event object by a given id.
        '''
        eventRows = {}
        try:
            self._cur.execute(
                'SELECT id, name, creator_id, created_date from event WHERE id={0}'
                .format(eventId)
            )
            eventData = self._cur.fetchone()

        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException('Unknown error when loading event')

        if (len(eventData) > 0):
            # ID is primary key. Should only ever get 1 or 0
            data = {}
            data['id'] = eventData[0]
            data['name'] = eventData[1]
            data['creator_id'] = eventData[2]
            data['created_date'] = eventData[3]
            return data
        else:
            # not found
            print('Given ID was not found', eventId)
            raise DaoException('Unknown error when loading event')

    def load_attendee_events (self, attendee_id):
        '''
        Loads all events that the attendee is attending.
        '''
        eventRows = {}
        try:
            self._cur.execute(
                'SELECT events.id, events.name, events.creator_id, ' +
                'events.created_date FROM events INNER JOIN event_attendees ' +
                'ON event_attendees.event_id = events.id AND ' +
                'event_attendees.attendee_id = {0}'
                .format(attendee_id)
            )
            eventRows = self._cur.fetchall()

        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException('Unknown error when loading event')

        data = []
        for event in eventRows:
            tempData = {}
            tempData['id'] = event[0]
            tempData['name'] = event[1]
            tempData['creator_id'] = event[2]
            tempData['created_date'] = event[3]
            data.append(tempData)

        return data

    def save_event(self, eventObject):
        '''
        Generates a unique ID for the event and creates a new instance in the database.

        An attendee can be in multiple events. Creator ID is stored as a cookie.
        When joining an event, a creator ID is either generated and saved, or it
        is retrieved from the cookies.
        '''

        try:
            # generate an initial id based on event name
            generatedId = HashCodeUtils.generate_code(eventObject['name'])

            # if the id is taken, append characters and re-generate
            count = 0
            newSeed = eventObject['name'] + 'a';
            while count < 5:
                if (self.event_exists(generatedId)):
                    break
                generatedId = HashCodeUtils.generate_code(newSeed)
                newSeed = newSeed + 'a'
                count += 1

            # after 5 tries, check if id is still taken...
            if not self.event_exists(generatedId):
                # ... save if id is unique
                self._cur.execute(
                    'INSERT INTO event (id, name, creator_id, created_date) '
                    'VALUES (\'{0}\', \'{1}\', {2}, \'{3}\')'.format(
                        generatedId,
                        eventObject['name'],
                        eventObject['creator_id'],
                        datetime.datetime.now().strftime('%Y%m%d')
                    )
                )

                # ... and update the event_attendee join table
                self._cur.execute(
                    'INSERT INTO event_attendee (event_id, creator_id) '
                    'VALUES (\'{0}\', {1})'.format(
                        generatedId,
                        eventObject['creator_id']
                    )
                )

                return self.load_event(generatedId)

            # ... raise an exception if not
            else:
                raise DaoException(
                    'Unable to generate a unique ID. Please choose a new name.'
                )

        # Throw any DaoExceptions. Catch anything else.
        except DaoException as e:
            raise e
        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException(
                'An error occurred saving this event. Please try again later.'
            )

        print(eventObject)

    def update_event(self, eventObject):
        try:
            self._cur.execute(
                'INSERT INTO event (name) VALUES (\'{0}\') '
                'WHERE id={1}'.format(
                    eventObject['name'],
                    eventObject['id']
                )
            )
            return self._cur.fetchone()
        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException('Unknown error while updating event')

    def delete_event(self, event_id):
        '''
        Deletes the event with the given id.

        If successful, this function returns nothing. THrows exception otherise.
        '''

        try:
            # delete the event
            self._cur.execute(
                'DELETE FROM event WHERE id={0}'.format(event_id)
            )
            # delete event_attendee entries
            self._cur.execute(
                'DELETE FROM event_attendee WHERE event_id={0}'.format(
                    event_id
                )
            )
        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException(
                'An error occurred deleting this event. Please try again later.'
            )
