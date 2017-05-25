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
				# check if creator id was provided...
				creator_id = ''
				if 'creator_id' not in req_body or req_body['creator_id'] is None:
					# ... create a new attendee record if not
					ctr = self.__attendee_dao.save_attendee({
						'name': eventObject['creator']
					})
					creator_id = ctr['id']
				else:
					# ... or use the one provided
					creator_id = eventObject['creator_id']

				# set the creator_id and save the event
				req_body['creator_id'] = creator_id
				data = self.__event_dao.save_event(req_body)

				# build the response body
				json_data = json.dumps(data)
				response_body = json_data

			else:
				response_body = json.dumps(inputErrors)
		except (DaoException, ValidationException) as e:
			raise ServiceException(e.message)

		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException('An error occurred while creating this event.')

		return response_body

	def delete_event (self, req_body):
		try:
			inputErrors = inputValidator.validate_event(req_body)
			self.__event_dao.delete_event(req_body)
		except (DaoException, ValidationException) as e:
			raise ServiceException(e.message)

	def add_event_attendee (self, req_body, event_id):
		try:
			inputErrors = inputValidator.validate_event(req_body)
			self.__attendee_dao.join_event(req_body, event_id)
		except (DaoException, ValidationException) as e:
			raise ServiceException(e.message)
		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException(
				'An error occurred while joining this event.'
			)

	def update_attendee (self, req_body):
		response_body = {}
		try:
			inputErrors = inputValidator.validate_attendee(req_body)
			data = self.__attendee_dao.update_attendee(req_body)
			json_data = json.dumps(data)
			response_body = json_data
		except (DaoException, ValidationException) as e:
			raise ServiceException(e.message)
		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException(
				'An error occurred while updating your info.'
			)
		return response_body

	def delete_event_attendee (self, req_body, event_id):
		try:
			inputErrors = inputValidator.validate_event(req_body)
			self.__event_dao.leave_event(req_body, event_id)
		except (DaoException, ValidationException) as e:
			raise ServiceException(e.message)
		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException(
				'An error occurred while leaving this info.'
			)

	def update_attendee_availability (self, req_body):
		pass
