import os
import sys
import importlib
from classes.exception.DaoException import DaoException
from classes.HashCodeUtils import HashCodeUtils

psycopg2 = {}

try:
	if os.environ['ENV'] == 'test':
		temp = importlib.import_module('test.classes.Psycopg2')
		psycopg2 = temp.psycopg2()
	else:
		psycopg2 = __import__('psycopg2')
except ImportError:
	print(ImportError)

class AttendeeDao:

	__cur = {}

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

	def save_attendee (self, attendee):
		self.__cur.execute(
			'INSERT INTO atendee (name) VALUES ({0})'.format(
				attendee['creator']
			)
		)
		return self.__cur.fetchone()

	def attendee_exists (self, attendee_id):
		try:
			self.__cur.execute(
				'SELECT id name email FROM attendee WHERE id = {0}'.format(attendee_id)
			)
			return self.__cur.fetchone() is not None
		except Exception as e:
			print(e, sys.exc_info())
			raise DaoException('Unknown error when searching for attendee')
