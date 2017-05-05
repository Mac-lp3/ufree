import os
import psycopg2
import classes.exception.DaoException as DaoException
from classes.HashCodeUtils import HashCodeUtils

class EventDao:

	try:
		db_conn_str = 'dbname=' + os.environ['DB_NAME']
		conn = psycopg2.connect(db_conn_str)
		cur = conn.cursor()
	except:
		cur = {}
		print('I am unable to connect to the database')

	def event_exists(eventId):

		EventDao.cur.execute('SELECT name FROM events WHERE id = {0}'.format(eventId))
		return EventDao.cur.fetchone() is not None

	def load_event(eventId):
		'''
		Loads an event object by a given id.
		'''

		EventDao.cur.execute('SELECT id, name from events WHERE id=' + str(eventId))
		eventRows = EventDao.cur.fetchall()

		EventDao.cur.execute('SELECT id, creator, fromdate, todate from dateRanges WHERE eventid=' + str(eventId))
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

	def save_event(eventObject):
		'''
		Generates a unique ID for the event and creates a new instance in the database.
		'''

		# generate an initial id based on event name
		generatedId = HashCodeUtils.generate_code(eventObject['name'])

		try:

			# if the id is taken, append characters and re-generate
			count = 0
			newSeed = eventObject['name'] + 'a';
			while EventDao.event_exists(generatedId) and count < 5:
				generatedId = HashCodeUtils.generate_code(newSeed)
				newSeed = newSeed + 'a'

			# If after 5 tries, check if the ID is unique and save if so.
			if not EventDao.event_exists(generatedId):
				EventDao.cur.execute('INSERT INTO events (id, name) VALUES ({0}, \'{1}\')'.format(generatedId, eventObject['name']))
				return EventDao.load_event(generatedId)

			# Raise an exception if not.
			else:
				raise DaoException('Unable to generate a unique ID. Please choose a new name.')

		# Catch any general exceptions
		except psycopg2.Error as e:
			print(e.pgerror)
			raise DaoException('An error occurred saving this event. Please try again later.')

		print(eventObject)

	def update_event(eventObject):

		# TODO update date ranges
		EventDao.cur.execute('INSERT INTO events (name) VALUES (\'{0}\') WHERE eventid={1}'.format(eventObject['name']), eventObject['id'])

	def delete_event(eventObject):
		'''
		Deletes the event with the given eventHash and all associated date ranges.

		If successful, this function returns nothing. A corresponding exception is thrown
		otherwise.
		'''

		try:
			EventDao.cur.execute('DELETE FROM events WHERE id={0}'.format(eventObject['id']))
		except psycopg2.Error as e:
			print(e.pgerror)
			raise DaoException('An error occurred deleting this event. Please try again later.')

	def add_date_range(eventId, dateRange):
		#TODO
		pass
