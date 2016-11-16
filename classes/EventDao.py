import psycopg2

class EventDao:

	try:
		conn = psycopg2.connect("dbname='ufree'")
		cur = conn.cursor()
	except:
		cur = {}
		print("I am unable to connect to the database")

	def load_event(eventId):
		"""
		Loads an event object by a given id.
		"""

		EventDao.cur.execute("SELECT id, name from events WHERE id=" + str(eventId))
		eventRows = EventDao.cur.fetchall()

		EventDao.cur.execute("SELECT id, creator, fromdate, todate from dateRanges WHERE eventid=" + str(eventId))
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

		# TODO hash generation
		EventDao.cur.execute('INSERT INTO events (name) VALUES (\'{0}\')'.format(eventObject['name']))

		print(eventObject)

	def update_event(eventObject):

		# TODO update date ranges
		EventDao.cur.execute('INSERT INTO events (name) VALUES (\'{0}\') WHERE eventid={1}'.format(eventObject['name']), eventObject['id'])

	def delete_event(eventObject):
		"""
		Deletes the event with the given eventHash and all associated date ranges.

		 If successful, this function returns nothing. A corresponding exception is thrown
		otherwise.
		"""
		
		try:
			EventDao.cur.execute('DELETE FROM events WHERE id={0}'.format(eventObject['id']))
		except psycopg2.Error as e:
			print(e.pgerror)
	    	raise Exception('An error occurred deleting this event. Please try again later.')

	def add_date_range(eventId, dateRange):
		#TODO

		