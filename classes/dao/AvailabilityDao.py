import os
import sys
import importlib
import datetime
from classes.exception.DaoException import DaoException
from classes.util.HashCodeUtils import HashCodeUtils

psycopg2 = {}

if os.environ['ENV'] == 'test':
	temp = importlib.import_module('test.classes.Psycopg2')
	psycopg2 = temp.psycopg2()
else:
	psycopg2 = __import__('psycopg2')

class AvailbilityDao:

	def __init__ (self):
		try:
			db_conn_str = 'dbname=' + os.environ['DB_NAME']
			conn = psycopg2.connect(db_conn_str)
			self.__cur = conn.cursor()
		except ImportError:
			print(ImportError)
		except:
			print(sys.exc_info())
			print('I am unable to connect to the database')

	def get_event_availability (self):
		'''
		compiles list of all availablity for this event
		'''
		pass

	def get_attendee_availability (self):
		'''
		gets this users availability
		'''
		pass

	def update_availability (self):
		'''
		Updates this users availability for this event
		'''
		pass

	def delete_availability (self):
		'''
		removes this users availability from the event.
		'''
		pass

	def create_availability(self):
		'''
		adds entry to the join table. adds a row of 0s for this user/event
		'''
		pass
