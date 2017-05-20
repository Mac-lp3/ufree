import os
import unittest
import builtins
from classes.dao.EventDao import EventDao
from classes.exception.DaoException import DaoException

class EventDaoTest(unittest.TestCase):

    def setUp (self):
        builtins.db_fail = os.environ['TEST_DB_FAIL']
        self.__dao = EventDao()

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
        builtins.return_pattern = [{'id': 'idk'}, None, None, [['abcd1234']]]
        val = self.__dao.save_event({
            'name': 'Some cool thing',
            'creator': 'Mikey Big C'
        })
        self.assertTrue('id' in val)
        self.assertTrue('name' in val)
        self.assertTrue('creator_id' in val)

if __name__ == '__main__':
	unittest.main()
