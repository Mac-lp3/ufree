import os
import sys
import json
import inspect
import importlib
from classes.util.HashCodeUtils import HashCodeUtils
from classes.util.EventValidator import EventValidator
from classes.util.AttendeeValidator import AttendeeValidator
from classes.exception.ServiceException import ServiceException
from classes.exception.BaseAppException import BaseAppException

class EventService:

	def __init__ (self):
		# init DAOs based on environment
		self.__eventValidator = EventValidator()
		self.__attendeeValidator = AttendeeValidator()
		if os.environ['ENV'] == 'test':
			temp = importlib.import_module('test.classes.EventDao')
			self.__event_dao = temp.EventDao()
			temp = importlib.import_module('test.classes.AttendeeDao')
			self.__attendee_dao = temp.AttendeeDao()
			temp = importlib.import_module('test.classes.AvailabilityDao')
			self.__availability_dao = temp.AvailabilityDao()
		else:
			temp = importlib.import_module('classes.dao.EventDao')
			self.__event_dao = temp.EventDao()
			temp = importlib.import_module('classes.dao.AttendeeDao')
			self.__attendee_dao = temp.AttendeeDao()
			temp = importlib.import_module('classes.dao.AvailabilityDao')
			self.__availability_dao = temp.AvailabilityDao()

	def load_event (self, event_id):
		response_body = {}
		try:
			data = self.__event_dao.load_event(event_id)
			json_data = json.dumps(data)
			response_body = json_data
		except BaseAppException as e:
			raise ServiceException(str(e))
		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException(
				'An error occurred while loading this event.'
			)
		return response_body

	def update_event (self, req_body):
		response_body = {}
		try:
			payload = req_body.json_body
			self.__eventValidator.validate_event(payload)
			data = self.__event_dao.update_event(payload)
			json_data = json.dumps(data)
			response_body = json_data
		except BaseAppException as e:
			raise ServiceException(str(e))
		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException(
				'An error occurred while updating this event.'
			)
		return response_body

	def create_event (self, req):
		'''
		Creates a new event.

		Validates the request object, extracts all required information, and
		builds the event and associated objects.
		'''
		# TODO year mechanism.
		response_body = {}
		try:
			inputErrors = self.__eventValidator.validate_event(req.json_body)

			if not inputErrors:
				# set the creator_id and save the event
				req.json_body['creator_id'] = req.cookies['user_id']
				data = self.__event_dao.save_event(req.json_body)

				# build the response body
				json_data = json.dumps(data)
				response_body = json_data

			else:
				response_body = json.dumps(inputErrors)
		except BaseAppException as e:
			raise ServiceException(str(e))

		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException('An error occurred while creating this event.')

		return response_body

	def delete_event (self, req):
		try:
			# validate event ID
			eventId = req.matchdict['eventId']
			inputErrors = self.__eventValidator.validate_event_id(eventId)

			# make sure this user is the creator
			user_id = req.cookies['user_id']
			event = self.__event_dao.load_event(eventId)

			# delete event if so
			if event['creator_id'] == user_id:
				self.__event_dao.delete_event(eventId)
			else:
				raise ServiceException(
					'Only the creator cannot delete this event'
				)
		except BaseAppException as e:
			raise ServiceException(str(e))

	def add_event_attendee (self, req):
		try:
			eventId = req.matchdict['eventId']
			self.__attendeeValidator.validate_attendee(req.json_body)
			self.__eventValidator.validate_event_id(eventId)
			self.__attendee_dao.join_event(req.json_body, eventId)
		except BaseAppException as e:
			raise ServiceException(str(e))
		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException(
				'An error occurred while joining this event.'
			)

	def update_attendee (self, req_body):
		response_body = {}
		try:
			inputErrors = self.__attendeeValidator.validate_attendee(req_body)
			data = self.__attendee_dao.update_attendee(req_body)
			json_data = json.dumps(data)
			response_body = json_data
		except BaseAppException as e:
			raise ServiceException(str(e))
		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException(
				'An error occurred while updating your info.'
			)
		return response_body

	def delete_event_attendee (self, req_body, event_id):
		try:
			# only creator or attendee should be able to do this.
			inputErrors = self.__eventValidator.validate_event_id(event_id)
			self.__event_dao.leave_event(req_body, event_id)
		except BaseAppException as e:
			raise ServiceException(str(e))
		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException(
				'An error occurred while leaving this info.'
			)

	def update_attendee_availability (self, req_body):
		response_body = {}
		try:
			# TODO validate availability
			#inputErrors = self.__eventValidator.validate_attendee(req_body)
			data = self.__availability_dao.update_availability(req_body)
			json_data = json.dumps(data)
			response_body = json_data
		except BaseAppException as e:
			raise ServiceException(str(e))
		except Exception as e:
			print(e, sys.exc_info())
			raise ServiceException(
				'An error occurred while updating availability.'
			)
		return response_body
