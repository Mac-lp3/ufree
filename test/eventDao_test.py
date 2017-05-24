import os
import unittest
import builtins
from classes.dao.EventDao import EventDao
from classes.exception.DaoException import DaoException

class EventDaoTest(unittest.TestCase):

	def setUp (self):
		builtins.db_fail = os.environ['TEST_DB_FAIL']
		self.__dao = EventDao()

	def delete_event_test (self):
		self.__dao.delete_event({
			'id': 'asdb1234',
			'name': 'idklol',
			'creator': 'someguy'
		})
		builtins.db_fail = 'True'
		try:
			self.__dao.delete_event({
				'id': 'asdb1234',
				'name': 'idklol',
				'creator': 'someguy'
			})
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))

	def update_event_test (self):
		# test normal behavior
		val = self.__dao.update_event({
			'id': 'abcd',
			'name': 'idklol'
		})
		self.assertTrue(val is not None)

		# test exception handling
		builtins.db_fail = 'True'
		try:
			val = self.__dao.update_event({
				'id': 'abcd',
				'name': 'idklol'
			})
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))

	def exists_test (self):
		# test normal functionality
		val = self.__dao.event_exists('some id')
		self.assertTrue(val)

		# test exception handling
		builtins.db_fail = 'True'
		try:
			val = self.__dao.event_exists('some id')
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))

	def load_event_test (self):
		# test normal functionality
		builtins.db_fail = 'False'
		val = self.__dao.load_event('some id')
		self.assertTrue('id' in val)
		self.assertTrue('name' in val)
		self.assertTrue('creator_id' in val)
		self.assertTrue('created_date' in val)

		# test exception handeling
		builtins.db_fail = 'True'
		try:
			val = self.__dao.load_event('some id')
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))

	def save_event_test (self):
		# test normal functionality
		builtins.return_pattern = [
			['name'],
			None,
			None,
			['idk', 'some name', 'some@email.com'],
			None,
			[['abcd1234']]
		]
		val = self.__dao.save_event({
			'name': 'Some cool thing',
			'creator': 'Mikey Big C'
		})
		self.assertTrue('id' in val)
		self.assertTrue('name' in val)
		self.assertTrue('creator_id' in val)

		# test unable to generate unique id
		builtins.return_pattern = [
			None,
			['name'],
			['name'],
			['idk', 'some name', 'some@email.com'],
			None,
			[['abcd1234']]
		]
		try:
			self.__dao.save_event({
				'name': 'Some cool thing',
				'creator': 'Mikey Big C'
			})
		except Exception as e:
			self.assertTrue(isinstance(e, DaoException))


if __name__ == '__main__':
	unittest.main()
