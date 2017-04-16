import json
import psycopg2
from classes.EventDao import EventDao
from classes.exception.DaoException import DaoException
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

	try:
		inputErrors = ApiInputValidator.validate_event(request.json_body)

		if not inputErrors:
			# hash is valid - save and return
			data = EventDao.save_event(request.json_body)
			json_data = json.dumps(data)
			return json_data

		else:
			# bad input
			response = HTTPBadRequest()
			response.text = json.dumps(inputErrors)
			response.content_type = 'application/json'

	except Exception as e:
		print(e)
		response = HTTPBadRequest()
		response.text = json.dumps({'errors': 'An error occurred while saving this event.'})
		response.content_type = 'application/json'

	return response

def get_event(request):
	"""
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	"""

	try:
		# validate
		eventId = request.matchdict['eventId']
		inputErrors = ApiInputValidator.validate_event_hash(eventId)

		if not inputErrors:
			data = EventDao.load_event(eventId)
			json_data = json.dumps(data)
			return json_data

		else:
			response = HTTPBadRequest()
			response.text = json.dumps(inputErrors)
			response.content_type = 'application/json'

	except Exception as e:
		print(e)
		response = HTTPBadRequest()
		response.text = json.dumps({'errors': 'An error occurred while loading this event.'})
		response.content_type = 'application/json'

	return response

def put_event(request):
	"""
	Update an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will update
	the one with the correspodning composite id.
	"""

	try:
		# validate sent object and its event hash
		inputErrors = ApiInputValidator.validate_event(request.json_body)
		inputErrors = inputErrors + ApiInputValidator.validate_event_hash(request.json_body['eventId'])

		if not inputErrors:
			data = EventDao.update_event(request.json_body)
			json_data = json.dumps(data)
			return json_data

		else:
			response = HTTPBadRequest()
			response.text = json.dumps(inputErrors)
			response.content_type = 'application/json'

	except Exception as e:
		print(e)
		response = HTTPBadRequest()
		response.text = json.dumps({'errors': 'An error occurred while updating this event.'})
		response.content_type = 'application/json'

	return response

def delete_event(request):
	"""
	Delete an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will delete
	the one with the correspodning composite id.
	"""

	try:
		# validate hash id
		eventId = request.matchdict['eventId']
		inputErrors = ApiInputValidator.validate_event_hash(eventId)

		if not inputErrors:
			EventDao.delete_event(request.json_body)
			response = Response(status=204)

		else:
			response = HTTPBadRequest()
			response.text = json.dumps({'errors': inputErrors})
			response.content_type = 'application/json'

	except DaoException as e:
		response = HTTPNotFound()
		response.text = json.dumps({'errors': 'No event with given id.'})
		response.content_type = 'application/json'

	except Exception as e:
		print(e)
		response = HTTPNotFound()
		response.text = json.dumps({'errors': 'An exception occurred deleting this event.'})
		response.content_type = 'application/json'

	return response

def post_date_range(request):
	"""
	Create a new date range associated with this event

	This will create a new date range with a generated composite id
	for this event.
	"""

	try:
		# validate event id and date range format
		eventId = request.matchdict['eventId']
		inputErrors = ApiInputValidator.validate_event_hash(eventId)
		inputErrors = inputErrors + ApiInputValidator.validate_date_range(request.json_body['dateRange'])

		if not inputErrors:
			# hash is valid - save and return
			data = EventDao.add_date_range(eventId, request.json_body)
			json_data = json.dumps(data)
			return json_data

		else:
			# bad input
			response = HTTPBadRequest()
			response.text = json.dumps(inputErrors)
			response.content_type = 'application/json'

	except Exception as e:
		print(e)
		response = HTTPBadRequest()
		response.text = json.dumps({'errors': 'An exception occurred while handeling new date range.'})
		response.content_type = 'application/json'

	return response

def includeme(config):

	config.add_route('eventBase', '/api/events')
	config.add_renderer('eventBase', 'pyramid.renderers.json_renderer_factory')

	config.add_route('eventDetails', '/api/events/{eventId}')
	config.add_renderer('eventDetails', 'pyramid.renderers.json_renderer_factory')

	config.add_route('rangesBase', '/api/events/{eventId}/ranges')
	config.add_renderer('rangesBase', 'pyramid.renderers.json_renderer_factory')

	config.add_route('rangeDetails', '/api/events/{eventId}/ranges/{rangeId}')
	config.add_renderer('rangeDetails', 'pyramid.renderers.json_renderer_factory')

	# creates new date and generates an id
	config.add_view(post_event, route_name='eventBase', request_method="POST", renderer="json")

	# returns the event object + children
	config.add_view(get_event, route_name='eventDetails', request_method="GET", renderer='json')

	# updates the event (new/updated date range)
	config.add_view(put_event, route_name='eventDetails', request_method="PUT", renderer="json")

	# deletes an event
	config.add_view(delete_event, route_name='eventDetails', request_method="DELETE")

	# creates a new date range
	config.add_view(post_date_range, route_name='rangesBase', request_method="POST", renderer="json")
