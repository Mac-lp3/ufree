import os
import unittest
import builtins
from classes.dao.AttendeeDao import AttendeeDao
from classes.exception.DaoException import DaoException

class AttendeeDaoTest(unittest.TestCase):

	def setUp (self):
		builtins.db_fail = os.environ['TEST_DB_FAIL']
		self.__dao = AttendeeDao()

	def load_attendee_test (self):
		# test normal functionality
		builtins.db_fail = 'False'
		builtins.return_pattern = [
			['idk', 'some name', 'some@email.com'],
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
