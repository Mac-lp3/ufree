import os
import sys
import importlib
import datetime
from classes.exception.DaoException import DaoException
from classes.util.HashCodeUtils import HashCodeUtils

psycopg2 = {}

if os.environ['ENV'] == 'test':
    temp = importlib.import_module('test.classes.Psycopg2')
    psycopg2 = temp.psycopg2()
else:
    psycopg2 = __import__('psycopg2')

class AvailbilityDao:

    def __init__ (self):
        try:
            db_conn_str = 'dbname=' + os.environ['DB_NAME']
            conn = psycopg2.connect(db_conn_str)
            self.__cur = conn.cursor()
        except ImportError:
            print(ImportError)
        except:
            print(sys.exc_info())
            print('I am unable to connect to the database')

    def get_availability (self, attendee_id='', event_id=''):
        '''
        gets this users availability
        '''
        try:

            if attendee_id:
                if event_id:
                    self.__cur.execute(
                        'SELECT id, attendee_id, event_id, year, january, '
                        'february, march, april, may, june, july, august, '
                        'september, october, november, december FROM '
                        'availability WHERE attendee_id={0} AND event_id=\'{1}\''
                        .format(
                            availability['attendee_id'],
                            availability['event_id']
                        )
                    )
                else:
                    self.__cur.execute(
                        'SELECT id, attendee_id, event_id, year, january, february, '
                        'march, april, may, june, july, august, september, october, '
                        'november, december FROM availability WHERE attendee_id='.format(
                            availability['attendee_id']
                        )
                    )
            else:
                self.__cur.execute(
                    'SELECT id, attendee_id, event_id, year, january, '
                    'february, march, april, may, june, july, august, '
                    'september, october, november, december FROM '
                    'availability WHERE event_id={0}'.format(
                        availability['event_id']
                    )
                )

            at = self.__cur.fetchone()

            data = {
                'id': at[0],
                'attendee_id': at[1],
                'event_id': at[2],
                'year': at[3],
                'january': at[4],
                'february': at[5],
                'march': at[6],
                'april': at[7],
                'may': at[8],
                'june': at[9],
                'july': at[10],
                'august': at[11],
                'september': at[12],
                'october': at[13],
                'november': at[14],
                'december': at[15]
            }

            return data

        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException(
                'Unknown error while saving availability'
            )

    def update_availability (self, availability):
        '''
        Updates this users availability for this event
        '''
        try:
            self.__cur.execute(
                'INSERT INTO availability ('
                january, february, march, '
                'april, may, june, july, august, september, october, '
                'november, december) VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', '
                '\'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\', \'{10}\', '
                '\'{11}\') WHERE id={12}'.format(
                    availability['january'],
                    availability['february'],
                    availability['march'],
                    availability['april'],
                    availability['may'],
                    availability['june'],
                    availability['july'],
                    availability['august'],
                    availability['september'],
                    availability['october'],
                    availability['november'],
                    availability['december'],
                    availability['id']
                )
            )

            at = self.__cur.fetchone()

            data = {
                'id': at[0],
                'attendee_id': at[1],
                'event_id': at[2],
                'year': at[3],
                'january': at[4],
                'february': at[5],
                'march': at[6],
                'april': at[7],
                'may': at[8],
                'june': at[9],
                'july': at[10],
                'august': at[11],
                'september': at[12],
                'october': at[13],
                'november': at[14],
                'december': at[15]
            }

            return data

        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException(
                'Unknown error while updaing availability'
            )

    def delete_availability (self, availability_id, attendee_id='', event_id=''):
        '''
        removes this users availability from the event.
        '''
        try:
            if attendee_id:
                if event_id:
                    self.__cur.execute(
                        'DELETE FROM availability WHERE attendee_id={0} '
                        'AND event_id=\'{1}\''.format(
                            attendee_id,
                            event_id
                        )
                    )
                else:
                    self.__cur.execute(
                        'DELETE FROM availability WHERE attendee_id={0}'.format(
                            attendee_id
                        )
                    )
            elif event_id
                self.__cur.execute(
                        'DELETE FROM availability WHERE event_id={0}'.format(
                            event_id
                        )
                    )
            else:
                self.__cur.execute(
                    'DELETE FROM availability WHERE id={0}'.format(
                        availability_id
                    )
                )
        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException(
                'Unknown error while deleting availability'
            )

    def save_availability(self, availability):
        '''
        adds entry to the join table. adds a row of 0s for this user/event
        '''
        # TODO year check for multiple vailaibility

        try:
            self.__cur.execute(
                'INSERT INTO availability ('
                'attendee_id, event_id, year, january, february, march, '
                'april, may, june, july, august, september, october, '
                'november, december) VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', '
                '\'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\', \'{10}\', '
                '\'{11}\', \'{12}\', \'{13}\', \'{14}\')'.format(
                    availability['attendee_id'],
                    availability['event_id'],
                    availability['year'],
                    availability['january'],
                    availability['february'],
                    availability['march'],
                    availability['april'],
                    availability['may'],
                    availability['june'],
                    availability['july'],
                    availability['august'],
                    availability['september'],
                    availability['october'],
                    availability['november'],
                    availability['december']
                )
            )

            at = self.__cur.fetchone()

            data = {
                'id': at[0],
                'attendee_id': at[1],
                'event_id': at[2],
                'year': at[3],
                'january': at[4],
                'february': at[5],
                'march': at[6],
                'april': at[7],
                'may': at[8],
                'june': at[9],
                'july': at[10],
                'august': at[11],
                'september': at[12],
                'october': at[13],
                'november': at[14],
                'december': at[15]
            }

            return data

        except Exception as e:
            print(e, sys.exc_info())
            raise DaoException(
                'Unknown error while saving availability'
            )
