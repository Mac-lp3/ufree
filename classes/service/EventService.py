import os
import sys
import json
import inspect
import importlib
from classes.util.HashCodeUtils import HashCodeUtils
from classes.exception.DaoException import DaoException
from classes.util.ApiInputValidator import ApiInputValidator
from classes.exception.ServiceException import ServiceException
from classes.exception.ValidationException import ValidationException

class EventService:

	def __init__ (self):
		# init DAOs based on environment
		if os.environ['ENV'] == 'test':
			temp = importlib.import_module('test.classes.EventDao')
			self.__event_dao = temp.EventDao()
			temp = importlib.import_module('test.classes.AttendeeDao')
			self.__attendee_dao = temp.AttendeeDao()
		else:
			temp = importlib.import_module('classes.dao.EventDao')
			self.__event_dao = temp.EventDao()
			temp = importlib.import_module('classes.dao.AttendeeDao')
			self.__attendee_dao = temp.AttendeeDao()

	def create_event (self, req_body):
		'''
		Creates a new event.

		Validates the request object, extracts all required information, and
		builds the event and associated objects.
		'''

		response_body = {}
		try:
			inputErrors = inputValidator.validate_event(req_body)

			if not inputErrors:
				creator_id = ''
				# check if creator id was provided...
				if 'creator_id' not in req_body or req_body['creator_id'] is None:
					# ...create a new attendee record if not
					ctr = self.__attendee_dao.save_attendee({
						'name': eventObject['creator']
					})
					creator_id = ctr['id']
				else:
					# ... or use the one provided
					creator_id = eventObject['creator_id']

				req_body['creator_id'] = creator_id
				data = self.__event_dao.save_event(req_body)
				json_data = json.dumps(data)
				response_body = json_data

			else:
				response_body = json.dumps(inputErrors)
		except DaoException as e:
			raise ServiceException(e.message)

		except Exception as e:
			print(e, sys.exc_info())
			response_body = json.dumps({
				'error': 'An error occurred while creating this event.'
			})

		return response_body

	def delete_event (self, req_body):
		pass

	def add_event_attendee (self, req_body):
		pass

	def update_event_attendee (self, req_body):
		pass

	def delete_event_attendee (self, req_body):
		pass

	def update_attendee_availability (self, req_body):
		pass
