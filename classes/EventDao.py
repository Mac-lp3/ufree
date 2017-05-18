import os
import sys
import importlib
from classes.exception.DaoException import DaoException
from classes.HashCodeUtils import HashCodeUtils

psycopg2 = {}

try:
	if os.environ['ENV'] == 'test':
		temp = importlib.import_module('test.classes.Psycopg2')
		psycopg2 = temp.psycopg2()
	else:
		psycopg2 = __import__('psycopg2')
except ImportError:
	print(ImportError)

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
			self.__cur.execute('SELECT name FROM events WHERE id = {0}'.format(eventId))
			return self.__cur.fetchone() is not None
		except Exception as e:
			print(e, sys.exc_info())
			raise DaoException('Unknown error when searching for event')

	def load_event(self,eventId):
		'''
		Loads an event object by a given id.
		'''
		try:
			self.__cur.execute('SELECT id, name from events WHERE id=' + str(eventId))
			eventRows = self.__cur.fetchall()

			self.__cur.execute('SELECT id, creator, fromdate, todate from dateRanges WHERE eventid=' + str(eventId))
			dateRangeRows = EventDao.cur.fetchall()

			if (len(eventRows) == 1):
				# Single record found.
				# built the return object
				dateRangeData = []
				for dateRange in dateRangeRows:
					dateRangeData.append({
						'id': dateRange[0],
						'creator': dateRange[1],
						'fromDate': dateRange[2],
						'toDate': dateRange[3]
					})

				data = {}
				data['id'] = eventRows[0][0]
				data['name'] = eventRows[0][1]
				data['dateRanges'] = dateRangeData
				return data

			elif (len(eventRows) > 1):
				print('need to do a thing here')

			else:
				# ID doesn't exist
				# raise HTTPNotFound
				print('need to do a thing here')
		except Exception as e:
			print(e, sys.exc_info())
			raise DaoException('Unknown error when loading event')

	def save_event(self, eventObject):
		'''
		Generates a unique ID for the event and creates a new instance in the database.
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

			# If after 5 tries, check if the ID is unique and save if so.
			if not self.event_exists(generatedId):
				self.__cur.execute('INSERT INTO events (id, name) VALUES ({0}, \'{1}\')'.format(generatedId, eventObject['name']))
				return EventDao.load_event(generatedId)

			# Raise an exception if not.
			else:
				raise DaoException('Unable to generate a unique ID. Please choose a new name.')

		# Catch any general exceptions
		except psycopg2.Error as e:
			print(e.pgerror)
			raise DaoException('An error occurred saving this event. Please try again later.')

		print(eventObject)

	def update_event(self, eventObject):

		# TODO update date ranges
		self.__cur.execute('INSERT INTO events (name) VALUES (\'{0}\') WHERE eventid={1}'.format(eventObject['name']), eventObject['id'])

	def delete_event(eventObject):
		'''
		Deletes the event with the given eventHash and all associated date ranges.

		If successful, this function returns nothing. A corresponding exception is thrown
		otherwise.
		'''

		try:
			self.__cur.execute('DELETE FROM events WHERE id={0}'.format(eventObject['id']))
		except psycopg2.Error as e:
			print(e.pgerror)
			raise DaoException('An error occurred deleting this event. Please try again later.')

	def add_date_range(self, eventId, dateRange):
		#TODO
		pass
