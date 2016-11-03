import json
import psycopg2
from classes.EventDao import EventDao
from classes.ApiInputValidator import ApiInputValidator
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPInternalServerError
from pyramid.view import view_config

def post_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	inputErrors = ApiInputValidator.validateEvent(request.json_body)

	try:
	
		if not inputErrors:

			# hash is valid - save and return
			data = EventDao.save_event(request.json_body)
			json_data = json.dumps(data)
			return json_data

		else:
			
			# bad input
			response = HTTPBadRequest()
			response.body = json.dumps(inputErrors)
			response.content_type = 'application/json'
			return response

	except Exception as e:
		print(e)
		raise HTTPInternalServerError

def get_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	try:

		# validate
		eventId = request.matchdict['eventId']
		inputErrors = ApiInputValidator.validateEventHash(eventId)

		if not inputErrors:
			data = EventDao.load_event(eventId)
			json_data = json.dumps(data)
			return json_data

		else:
			response = HTTPBadRequest()
			response.body = json.dumps(inputErrors)
			response.content_type = 'application/json'
			return response

	except Exception as e:
		print(e)
		raise HTTPInternalServerError

def put_event(request):
	"""
	Update an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will update
	the one with the correspodning composite id.
	"""

	try:
		# validate sent object and its event hash
		inputErrors = ApiInputValidator.validateEvent(request.json_body)
		inputErrors = inputErrors + ApiInputValidator.validateEventHash(request.json_body['eventId'])

		if not inputErrors:
			data = EventDao.update_event(request.json_body)
			json_data = json.dumps(data)
			return json_data

		else:
			response = HTTPBadRequest()
			response.body = json.dumps(inputErrors)
			response.content_type = 'application/json'
			return response

	except Exception as e:
		print(e)
		raise HTTPInternalServerError

def delete_event(request):
	"""
	Delete an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will delete
	the one with the correspodning composite id.
	"""

	# validate hash id
	eventId = request.matchdict['eventId']
	inputErrors = ApiInputValidator.validateEventHash(eventId)
	try: 
		if not inputErrors:
			# TODO check that something was deleted
			#data = EventDao.delete_event(request.json_body)
			data = ['value']
			if data:
				response = Response(status=204)
			else:
				response = HTTPNotFound()
				response.text = json.dumps({'errors': 'No event with given id.'})
				response.content_type = 'application/json'
		else:
			response = HTTPBadRequest()
			response.text = json.dumps({'errors': inputErrors})
			response.content_type = 'application/json'

		return response

	except Exception as e:
		print(e)
		raise HTTPInternalServerError

def post_date_range(request):
	"""
	Create a date rang in this eventDetails

	This will create a new date range with a generated composite id
	for this eventDetails.
	"""

	try:

		# validate event id and date range format
		eventId = request.matchdict['eventId']
		inputErrors = ApiInputValidator.validateEventHash(eventId)
		inputErrors = inputErrors + ApiInputValidator.validateDateRange(request.json_body['dateRange'])

		if not inputErrors:

			# hash is valid - save and return
			data = EventDao.add_date_range(eventId, request.json_body)
			json_data = json.dumps(data)
			return json_data

		else:
			
			# bad input
			response = HTTPBadRequest()
			response.body = json.dumps(inputErrors)
			response.content_type = 'application/json'
			return response

	except ValueError:
		print("That's not an int!")
		raise HTTPBadRequest

	except Exception as e:
		print(e)
		raise HTTPInternalServerError

	postData = request.json_body

	return Response("Ya dang post")

def includeme(config):

	config.add_route('eventBase', '/api/event')
	config.add_renderer('eventBase', 'pyramid.renderers.json_renderer_factory')

	config.add_route('eventDetails', '/api/event/{eventId}')
	config.add_renderer('eventDetails', 'pyramid.renderers.json_renderer_factory')

	config.add_route('rangesBase', '/api/event/{eventId}/ranges')
	config.add_renderer('rangesBase', 'pyramid.renderers.json_renderer_factory')

	config.add_route('rangeDetails', '/api/event/{eventId}/ranges/{rangeId}')
	config.add_renderer('rangeDetails', 'pyramid.renderers.json_renderer_factory')

	# creates new date and generates an id
	config.add_view(post_event, route_name='eventBase', request_method="POST", renderer="json")

	# returns the event object + children
	config.add_view(get_event, route_name='eventDetails', request_method="GET", renderer='json')

	# updates the event (new/updated date range)
	config.add_view(put_event, route_name='eventDetails', request_method="PUT", renderer="json")

	# deletes an event
	config.add_view(delete_event, route_name='eventDetails', request_method="DELETE")
