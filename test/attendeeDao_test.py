import os
import unittest
import builtins
from classes.dao.AttendeeDao import AttendeeDao
from classes.exception.DaoException import DaoException

class AttendeeDaoTest(unittest.TestCase):

	def setUp (self):
		builtins.db_fail = os.environ['TEST_DB_FAIL']
		self.__dao = AttendeeDao()

	def delete_attendee_test (self):
		self.__dao.delete_attendee({
			'id': 'asdb1234',
			'name': 'idklol'
		})
		builtins.db_fail = 'True'
		try:
			self.__dao.delete_attendee({
				'id': 'asdb1234',
				'name': 'idklol'
			})
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))

	def update_attendee_test (self):
		# test normal behavior
		val = self.__dao.update_attendee({
			'id': 'abcd',
			'name': 'idklol',
			'email': 'lol@idk.gov'
		})
		self.assertTrue(val is not None)

		# test exception handling
		builtins.db_fail = 'True'
		try:
			val = self.__dao.update_attendee({
				'id': 'abcd',
				'name': 'idklol',
				'email': 'lol@idk.gov'
			})
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))

	def attendee_exists_test (self):
		# test normal functionality
		val = self.__dao.attendee_exists('some id')
		self.assertTrue(val)

		# test exception handling
		builtins.db_fail = 'True'
		try:
			val = self.__dao.attendee_exists('some id')
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))

	def load_attendee_test (self):
		# test normal functionality
		builtins.db_fail = 'False'
		builtins.return_pattern = [
			['idk', 'some name', 'some@email.com']
		]
		val = self.__dao.load_attendee('some id')
		self.assertTrue('id' in val)
		self.assertTrue('name' in val)
		self.assertTrue('email' in val)

		# test exception handeling
		builtins.db_fail = 'True'
		try:
			val = self.__dao.load_attendee('some id')
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))

	def load_event_attendees_test (self):
		# test normal functionality
		builtins.db_fail = 'False'
		builtins.return_pattern = [
			['idk', 'some name', 'some@email.com'],
			['lol', 'some name', 'some@email.com'],
			['wat', 'some name', 'some@email.com'],
			['afk', 'some name', 'some@email.com'],
			['jk', 'some name', 'some@email.com']
		]
		val = self.__dao.load_event_attendees('some_event_id')
		print(val)
		self.assertTrue('id' in val)
		self.assertTrue('name' in val)
		self.assertTrue('email' in val)

		# test exception handeling
		builtins.db_fail = 'True'
		try:
			val = self.__dao.load_attendee('some id')
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))

	def save_attendee_test (self):
		# test normal functionality
		builtins.return_pattern = [
			['idk', 'some name', 'some@email.com'],
			['idk', 'some name', 'some@email.com']
		]
		val = self.__dao.save_attendee({
			'name': 'Some cool thing',
			'email': 'idk@lol.gov'
		})
		self.assertTrue('id' in val)
		self.assertTrue('name' in val)
		self.assertTrue('email' in val)

		# test unable to generate unique id
		builtins.db_fail = 'True'
		try:
			self.__dao.save_attendee({
				'name': 'Some cool thing',
				'email': 'idk@lol.gov'
			})
		except Exception as e:
			print(e)
			self.assertTrue(isinstance(e, DaoException))

	if __name__ == '__main__':
		unittest.main()
