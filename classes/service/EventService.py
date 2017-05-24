import os
import json
import inspect
import importlib
from classes.dao.AttendeeDao import AttendeeDao
from classes.exception.DaoException import DaoException

class EventService:

	def __init__ (self):
		if os.environ['ENV'] == 'test':
			temp = importlib.import_module('test.classes.EventDao')
			self.__event_dao = temp.EventDao()
		else:
			temp = importlib.import_module('classes.dao.EventDao')
			self.__event_dao = temp.EventDao()

	def create_event (self):
		pass

	def delete_event (self):
		pass

	def add_event_attendee (self):
		pass

	def update_event_attendee (self):
		pass

	def delete_event_attendee (self):
		pass

	def update_attendee_availability (self):
		pass
