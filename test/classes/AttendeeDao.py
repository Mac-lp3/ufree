import os
import sys
import importlib
from classes.exception.DaoException import DaoException

class AttendeeDao:

	def save_attendee (self, attendee):
		data = {
			'id': 'asd',
			'name': 'idkidkidk',
			'email': 'idk@lol.com'
		}
		return data

	def update_attendee (self, attendee):
		data = {
			'id': 'asd',
			'name': 'idkidkidk',
			'email': 'idk@lol.com'
		}
		return data

	def load_attendee (self, attendee_id):
		data = {
			'id': 'asd',
			'name': 'idkidkidk',
			'email': 'idk@lol.com'
		}
		return data

	def attendee_exists (self, attendee_id):
		return False

	def delete_attendee (self, attendee):
		pass
