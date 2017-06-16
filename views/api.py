import os
import json
import inspect
import importlib
from classes.exception.DaoException import DaoException
from classes.util.EventValidator import EventValidator
from classes.util.HashCodeUtils import HashCodeUtils
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPInternalServerError
from pyramid.view import view_config
from classes.exception.BaseAppException import BaseAppException
from classes.service.EventService import EventService

if os.environ['ENV'] == 'test':
	temp = importlib.import_module('test.classes.EventDao')
	EventDao = temp.EventDao()
	temp = importlib.import_module('test.classes.UserFilter')
	UserFilter = temp.UserFilter()
else:
	temp = importlib.import_module('classes.dao.EventDao')
	EventDao = temp.EventDao()
	temp = importlib.import_module('classes.filter.UserFilter')
	UserFilter = temp.UserFilter()

inputValidator = EventValidator()
__app_service = EventService()

def post_event(request):
	'''
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	'''
	try:
		filtered_request = UserFilter.set_user_id(request)
		payload = __app_service.create_event(filtered_request)
		response = Response(content_type='application/json')
		response.charset = 'UTF-8'
		response.json_body = payload
	except BaseAppException as e:
		response = HTTPBadRequest()
		response.text = e.get_payload()
		response.content_type = 'application/json'

	return response

def get_event(request):
	'''
	Get data for a specific event by ID.

	This returns the event object, populated by all date range objects
	'''
	response = {}
	try:
		filtered_request = UserFilter.set_user_id(request)
		payload = __app_service.load_event(filtered_request)
		response = Response(content_type='application/json')
		response.charset = 'UTF-8'
		response.json_body = payload
	except BaseAppException as e:
		response = HTTPBadRequest()
		response.text = e.get_payload()
		response.content_type = 'application/json'

	return response

def put_event(request):
	'''
	Update an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will update
	the one with the correspodning composite id.
	'''
	try:
		json_body = UserFilter.set_user_id(request.json_body)
		response = __app_service.update_event(json_body)
	except BaseAppException as e:
		response = HTTPBadRequest()
		response.text = e.get_payload()
		response.content_type = 'application/json'

	return response

def delete_event(request):
	'''
	Delete an existing date rang in this eventDetails

	If this eventDetails has existing date ranges, this will delete
	the one with the correspodning composite id.
	'''

	try:
		filtered_request = UserFilter.set_user_id(request)
		response = __app_service.delete_event(filtered_request)
	except BaseAppException as e:
		response = HTTPBadRequest()
		response.text = e.get_payload()
		response.content_type = 'application/json'

	return response

def post_date_range(request):
	'''
	Create a new date range associated with this event

	This will create a new date range with a generated composite id
	for this event.
	'''

	try:
		# validate event id and date range format
		eventId = request.matchdict['eventId']
		inputErrors = inputValidator.validate_event_hash(eventId)
		inputErrors = inputErrors + inputValidator.validate_date_range(request.json_body['dateRange'])

		if not inputErrors:
			# hash is valid - save and return
			data = EventDao.add_date_range(eventId, request.json_body)
			json_data = json.dumps(data)
			response = json_data

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
