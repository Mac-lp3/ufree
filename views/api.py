import json
import psycopg2
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
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

def delete_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	# go to DB and delete it.

	return Response("Delete an event") 

def put_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	# just a name change.
	# look up event, change the name, save it, return it

	return Response("Put an event") 

def get_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	#look for it in the DB.
	try:
		cur.execute("SELECT * from events WHERE id=1")
		rows = cur.fetchall()
		print(rows)
	except:
		print("lol, no");
	# return it if it is there. 404 else guess

	return Response("Got an event") 


# 
# event Api
#
def put_date_range(request):
	"""
	Update an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will update
	the one with the correspodning composite id.
	"""

	return Response("Ya dang put")

def delete_date_range(request):
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
		postData = request.json_body
		print(postData);
	except json.decoder.JSONDecodeError:
		print("no good mang")
		print(request)
		raise HTTPBadRequest

	postData = request.json_body

	return Response("Ya dang post")

def includeme(config):
	config.add_route('eventBase', '/api/event')
	config.add_renderer('eventBase', 'pyramid.renderers.json_renderer_factory')
	config.add_view(put_event, route_name='eventBase', request_method="PUT")
	config.add_view(post_event, route_name='eventBase', request_method="POST")
	config.add_view(delete_event, route_name='eventBase', request_method="DELETE")


	config.add_route('eventDetails', '/api/event/{hashId}')
	config.add_renderer('eventDetails', 'pyramid.renderers.json_renderer_factory')
	config.add_view(get_event, route_name='eventDetails', request_method="GET")
	config.add_view(put_date_range, route_name='eventDetails', request_method="PUT")
	config.add_view(post_date_range, route_name='eventDetails', request_method="POST")
	config.add_view(delete_date_range, route_name='eventDetails', request_method="DELETE")


