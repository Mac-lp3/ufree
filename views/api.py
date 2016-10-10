import json
import psycopg2
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

try:
	conn = psycopg2.connect("dbname='ufree'")
	cur = conn.cursor()
except:
	print("I am unable to connect to the database")

def post_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	# TODO
	# generate a unique ID/hash
	# just save it? they will all be unqie and the DB will generate the ID for you.
	# return the created object

	return Response("Post an event") 

def get_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	try:

		# validate
		hashId = int(request.matchdict['hashId'])
		cur.execute("SELECT id, name from events WHERE id=" + str(hashId))
		eventRows = cur.fetchall()

		cur.execute("SELECT id, creator, fromdate, todate from dateRanges WHERE eventid=" + str(hashId))
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
			json_data = json.dumps(data)
			return json_data

		elif (len(eventRows) > 1):
			print('need to do a thing here')

		else:
			# ID doesn't exist
			raise HTTPNotFound

	except ValueError:
   		print("That's not an int!")
   		raise HTTPBadRequest

	except:
		raise

def put_event(request):
	"""
	Update an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will update
	the one with the correspodning composite id.
	"""

	try: 

		# validate url param
		parsed_json = json.loads(request.json_body)
		hashId = int(request.matchdict['hashId'])

		curr.execute('INSERT INTO ')

	except ValueError:
   		print("That's not an int!")
   		raise HTTPBadRequest

	except:
		raise

	postData = request.json_body

	return Response("Ya dang post")

	return Response("Ya dang put")

def delete_event(request):
	"""
	Delete an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will delete
	the one with the correspodning composite id.
	"""

	return Response("Ya dang del")

def post_date_range(request):
	"""
	Create a date rang in this eventDetails

	This will create a new date range with a generated composite id
	for this eventDetails.
	"""

	try: 

		# validate
		parsed_json = json.loads(request.json_body)
		hashId = int(request.matchdict['hashId'])

		curr.execute('INSERT INTO ')

	except ValueError:
   		print("That's not an int!")
   		raise HTTPBadRequest

	except:
		raise

	postData = request.json_body

	return Response("Ya dang post")

def includeme(config):

	config.add_route('eventBase', '/api/event')
	config.add_renderer('eventBase', 'pyramid.renderers.json_renderer_factory')

	config.add_route('eventDetails', '/api/event/{hashId}')
	config.add_renderer('eventDetails', 'pyramid.renderers.json_renderer_factory')

	# creates new date and generates an id
	config.add_view(post_event, route_name='eventBase', request_method="POST")

	# returns the event object + children
	config.add_view(get_event, route_name='eventDetails', request_method="GET", renderer='json')

	# updates the event (new/updated date range)
	config.add_view(put_event, route_name='eventDetails', request_method="PUT")

	# deletes an event
	config.add_view(delete_event, route_name='eventDetails', request_method="DELETE")


