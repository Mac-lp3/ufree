import os
import sys
import importlib
from classes.dao.BaseDao import BaseDao
from classes.exception.DaoException import DaoException

psycopg2 = {}

try:
	if os.environ['ENV'] == 'test':
		temp = importlib.import_module('test.classes.Psycopg2')
		psycopg2 = temp.psycopg2()
	else:
		psycopg2 = __import__('psycopg2')
except ImportError:
	print(ImportError)

class AttendeeDao (BaseDao):

	__cur = {}

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

	def join_event (self, attendee, event_id):
		try:
			self.__cur.execute(
				'INSERT INTO event_attendee (event_id, creator_id) '
				'VALUES (\'{0}\', {1})'.format(
					event_id,
					attendee['id']
				)
			)
		except Exception as e:
			print(e, sys.exc_info(), attendee, event_id)
			raise DaoException(
				'Unknown error when adding attendee to event'
			)

	def leave_event (self, attendee_id, event_id):
		try:
			self.__cur.execute(
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
			self.__cur.execute(
				'INSERT INTO attendee (name) VALUES ({0})'.format(
					attendee['name']
				)
			)
			at = self.__cur.fetchone()
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
			self.__cur.execute(
				'INSERT INTO attendee (name, email) VALUES (\'{0}\', \'{1}\') '
				'WHERE id={2}'.format(
					attendee['name'],
					attendee['email'],
					attendee['id']
				)
			)
			return self.__cur.fetchone()
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
			self.__cur.execute(
				'SELECT attendee.id, attendee.name, attendee.email FROM attendee '
				'INNER JOIN event_attendee ON attendee.id=event_attendee.attendee_id '
				'WHERE event_attendee.event_id={0}'.format(
					event_id
				)
			)
			atts = self.__cur.fetchall()

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
			self.__cur.execute(
				'SELECT id, name, email from attendee WHERE id={0}'
				.format(attendee_id)
			)
			attendeeRows = self.__cur.fetchone()

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
			self.__cur.execute(
				'SELECT id name email FROM attendee WHERE id = {0}'.format(
					attendee_id
				)
			)
			return self.__cur.fetchone() is not None
		except Exception as e:
			print(e, sys.exc_info())
			raise DaoException('Unknown error when searching for attendee')

	def delete_attendee (self, attendee):
		try:
			# delete the attenddee
			self.__cur.execute(
				'DELETE FROM attendee WHERE id={0}'.format(attendee['id'])
			)
			# delete event_attendee entries
			self.__cur.execute(
				'DELETE FROM event_attendee WHERE attendee_id={0}'.format(
					attendee['id']
				)
			)
		except Exception as e:
			print(e, sys.exc_info())
			raise DaoException(
				'An error occurred deleting attendee. Please try again later.'
			)
