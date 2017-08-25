import os
import sys
import importlib
from classes.dao.BaseDao import BaseDao
from classes.exception.DaoException import DaoException

class AttendeeDao (BaseDao):

    def __init__ (self):
        BaseDao.__init__(self)

    def join_event (self, attendee_id, event_id):
        try:
            self._cur.execute(
                'INSERT INTO event_attendee (event_id, creator_id) '
                'VALUES (\'{0}\', {1})'.format(
                    event_id,
                    attendee_id
                )
            )
        except Exception as e:
            print(e, sys.exc_info(), attendee, event_id)
            raise DaoException(
                'Unknown error when adding attendee to event'
            )

    def leave_event (self, attendee_id, event_id):
        try:
            self._cur.execute(
                'DELETE FROM event_attendee WHERE event_id=\'{0}\' ' +
                'AND attendee_id={1}'.format(
                    event_id,
                    attendee_id
                )
            )

        except Exception as e:
            print(e, sys.exc_info(), attendee, event_id)
            raise DaoException(
                'Unknown error when removing attendee from event'
            )

    def save_attendee (self, attendee):
        try:
            self._cur.execute(
                'INSERT INTO attendee (name) VALUES ({0})'.format(
                    attendee['name']
                )
            )
            at = self._cur.fetchone()
            data = {
                'id': at[0],
                'name': at[1],
                'email': at[2]
            }
            return data
        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException(
                'Unknown error while saving attendee'
            )

    def update_attendee (self, attendee):
        try:
            self._cur.execute(
                'INSERT INTO attendee (name, email) VALUES (\'{0}\', \'{1}\') '
                'WHERE id={2}'.format(
                    attendee['name'],
                    attendee['email'],
                    attendee['id']
                )
            )
            return self._cur.fetchone()
        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException('Unknown error when loading attendee')

    def load_event_attendees (self, event_id):
        '''
        loads all attendees that are attending this event.

        Uses an inner join on the attendee and event_attendee table to retrieve
        the attendee data.
        '''
        try:
            # retrieve all event attendees from the DB
            self._cur.execute(
                'SELECT attendee.id, attendee.name, attendee.email FROM attendee '
                'INNER JOIN event_attendee ON attendee.id=event_attendee.attendee_id '
                'WHERE event_attendee.event_id={0}'.format(
                    event_id
                )
            )
            atts = self._cur.fetchall()

            # build a list of attendee objects
            att_list = []
            for att in atts:
                temp_att = {
                    'id': att[0],
                    'name': att[1],
                    'email': att[2]
                }
                att_list.append(temp_att)

            # return the built list
            return att_list

        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException('Unknown error when loading attendee')

    def load_attendee (self, attendee_id):
        attendeeRows = {}
        try:
            self._cur.execute(
                'SELECT id, name, email from attendee WHERE id={0}'
                .format(attendee_id)
            )
            attendeeRows = self._cur.fetchone()

        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException('Unknown error when loading attendee')

        if (attendeeRows is not None):
            # ID is primary key. Should only ever get 1 or 0
            data = {}
            data['id'] = attendeeRows[0]
            data['name'] = attendeeRows[1]
            data['email'] = attendeeRows[2]
            return data
        else:
            # not found
            print('Given id was not found', attendee['id'])
            raise DaoException('Attendee with this ID not found.')

    def attendee_exists (self, attendee_id):
        try:
            self._cur.execute(
                'SELECT id name email FROM attendee WHERE id = {0}'.format(
                    attendee_id
                )
            )
            return self._cur.fetchone() is not None
        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException('Unknown error when searching for attendee')

    def delete_attendee (self, attendee):
        try:
            # delete the attenddee
            self._cur.execute(
                'DELETE FROM attendee WHERE id={0}'.format(attendee['id'])
            )
            # delete event_attendee entries
            self._cur.execute(
                'DELETE FROM event_attendee WHERE attendee_id={0}'.format(
                    attendee['id']
                )
            )
        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException(
                'An error occurred deleting attendee. Please try again later.'
            )
