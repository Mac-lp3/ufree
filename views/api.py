import json
import psycopg2
from classes.EventDao import EventDao
from classes.ApiInputValidator import ApiInputValidator
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

def post_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	inputErrors = ApiInputValidator.validateEvent(request.json_body)
	
	if not inputErrors:

		# hash is valid
		dat = EventDao.save_event(request.json_body)

	else:
		
		# bad input
		response = HTTPBadRequest()
		response.body = json.dumps(inputErrors)
		response.content_type = 'application/json'
		return response

	return Response("Post an event") 

def get_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	try:

		# validate
		hashId = request.matchdict['hashId']
		inputErrors = ApiInputValidator.validateEventHash(hashId)
		
		if not inputErrors:
			data = EventDao.load_event(hashId)
			json_data = json.dumps(data)
			return json_data

		else:
			response = HTTPBadRequest()
			response.body = json.dumps(inputErrors)
			response.content_type = 'application/json'
			return response

	except:
		raise HTTPBadRequest

def put_event(request):
	"""
	Update an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will update
	the one with the correspodning composite id.
	"""

	try: 

		# validate url param
		hashId = int(request.matchdict['hashId'])
		parsed_json = json.loads(request.json_body)
		EventDao.save_event(parsed_json)

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
	config.add_view(post_event, route_name='eventBase', request_method="POST", renderer="json")

	# returns the event object + children
	config.add_view(get_event, route_name='eventDetails', request_method="GET", renderer='json')

	# updates the event (new/updated date range)
	config.add_view(put_event, route_name='eventDetails', request_method="PUT", renderer="json")

	# deletes an event
	config.add_view(delete_event, route_name='eventDetails', request_method="DELETE")
