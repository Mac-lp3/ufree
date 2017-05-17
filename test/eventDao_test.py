import os
import unittest
import builtins
from classes.EventDao import EventDao
from classes.exception.DaoException import DaoException

class EventDaoTest(unittest.TestCase):

    def setUp (self):
        builtins.db_fail = os.environ['TEST_DB_FAIL']
        self.__dao = EventDao()

    def exists_test (self):
        val = self.__dao.event_exists('some id')
        self.assertTrue(val)
        builtins.db_fail = 'True'
        try:
            val = self.__dao.event_exists('some id')
        except Exception as e:
            self.assertTrue(isinstance(e, DaoException))

if __name__ == '__main__':
	unittest.main()
