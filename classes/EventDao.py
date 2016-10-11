import psycopg2

try:
	conn = psycopg2.connect("dbname='ufree'")
	cur = conn.cursor()
except:
	print("I am unable to connect to the database")

def load_event(eventId):

	cur.execute("SELECT id, name from events WHERE id=" + str(eventId))
	eventRows = cur.fetchall()

	cur.execute("SELECT id, creator, fromdate, todate from dateRanges WHERE eventid=" + str(eventId))
	dateRangeRows = cur.fetchall()

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