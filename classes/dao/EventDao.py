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

class EventDao:

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

	def event_exists(self, eventId):
		try:
			self.__cur.execute('SELECT name FROM event WHERE id = {0}'.format(eventId))
			return self.__cur.fetchone() is not None
		except Exception as e:
			print(e, sys.exc_info())
			raise DaoException('Unknown error when searching for event')

	def load_event(self, eventId):
		'''
		Loads an event object by a given id.
		'''
		eventRows = {}
		try:
			self.__cur.execute(
				'SELECT id, name, creator_id, created_date from event WHERE id={0}'
				.format(eventId)
			)
			eventRows = self.__cur.fetchall()

		except Exception as e:
			print(e, sys.exc_info())
			raise DaoException('Unknown error when loading event')

		if (len(eventRows) == 1):
			# ID is primary key. Should only ever get 1 or 0
			data = {}
			data['id'] = eventRows[0][0]
			data['name'] = eventRows[0][1]
			data['creator_id'] = eventRows[0][2]
			data['created_date'] = eventRows[0][3]
			return data
		else:
			# not found
			print('Given ID was not found', eventId)
			raise DaoException('Unknown error when loading event')

	def save_event(self, eventObject):
		'''
		Generates a unique ID for the event and creates a new instance in the database.

		An attendee can be in multiple events. Creator ID is stored as a cookie.
		When joining an event, a creator ID is either generated and saved, or it
		is retrieved from the cookies.
		'''

		# generate an initial id based on event name
		generatedId = HashCodeUtils.generate_code(eventObject['name'])

		try:
			# if the id is taken, append characters and re-generate
			count = 0
			newSeed = eventObject['name'] + 'a';
			while self.event_exists(generatedId) and count < 5:
				generatedId = HashCodeUtils.generate_code(newSeed)
				newSeed = newSeed + 'a'
				count += 1

			# If after 5 tries, check if the ID is unique and save if so.
			if not self.event_exists(generatedId):
				# Check if a creator_id was provided...
				creatorId = ''
				if 'creator_id' not in eventObject or eventObject['creator_id'] is None:
					# create a new atendee if not
					self.__cur.execute(
						'INSERT INTO atendee (name) VALUES ({0})'.format(
							eventObject['creator']
						)
					)
					# ... and store the ID
					creatorId = self.__cur.fetchone()[0][0]
				else:
					# use the one provided if it exists
					creatorId = eventObject['creator_id']

				# save the event
				self.__cur.execute(
					'INSERT INTO event (id, name, creator_id, created_date)'
					' VALUES ({0}, \'{1}\', {2}, \'{3}\')'.format(
						generatedId,
						eventObject['name'],
						creatorId,
						datetime.datetime.now().strftime("%Y%m%d")
					)
				)

				# update the join table
				self.__cur.execute(
					'INSERT INTO event_attendee (event_id, creator_id)'
					' VALUES ({0}, {1})'.format(
						generatedId,
						creatorId
					)
				)

				return self.load_event(generatedId)

			# Raise an exception if not.
			else:
				raise DaoException('Unable to generate a unique ID. Please choose a new name.')

		# Throw any DaoExceptions. Catch anything else.
		except DaoException as e:
			raise e
		except Exception as e:
			print(str(e))
			raise DaoException('An error occurred saving this event. Please try again later.')

		print(eventObject)

	def update_event(self, eventObject):
		self.__cur.execute(
			'INSERT INTO events (name) VALUES (\'{0}\')'
			' WHERE event_id={1}'.format(
				eventObject['name'],
				eventObject['id']
			)
		)

	def delete_event(self, eventObject):
		'''
		Deletes the event with the given id.

		If successful, this function returns nothing. THrows exception otherise.
		'''

		try:
			# delete the event
			self.__cur.execute(
				'DELETE FROM event WHERE event_id={0}'.format(eventObject['id'])
			)
			# delete event_attendee entries
			self.__cur.execute(
				'DELETE FROM event_attendee WHERE event_id={0}'.format(
					eventObject['id']
				)
			)
		except Exception` as e:
			print(str(e))
			raise DaoException(
				'An error occurred deleting this event. Please try again later.'
			)
