import os
import unittest
import builtins
import test.classes.Const as const
from classes.dao.event_dao import EventDao
from classes.exception.dao_exception import DaoException

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
        builtins.db_return_object = [[
            const.GOOD_EVENT_ID,
            'some name',
            'some creator',
            'some date'
        ],[
            const.GOOD_EVENT_ID,
            'some name',
            'some creator',
            'some date'
        ]]
        val = self.__dao.event_exists(const.GOOD_EVENT_ID)
        self.assertTrue(val)

        # test exception handling
        builtins.db_fail = 'True'
        try:
            val = self.__dao.event_exists(const.GOOD_EVENT_ID)
        except Exception as e:
            self.assertTrue(isinstance(e, DaoException))

    def load_event_test (self):
        # test normal functionality
        builtins.db_fail = 'False'
        builtins.db_return_object = [[
            const.GOOD_EVENT_ID,
            'some name',
            'some creator',
            'some date'
        ]]
        val = self.__dao.load_event(const.GOOD_EVENT_ID)
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

    def load_attendee_events_test (self):
        # test normal functionality
        builtins.db_fail = 'False'
        builtins.db_return_object = [[
            const.GOOD_EVENT_ID,
            'some name',
            'some creator',
            'some date'
        ]]
        val = self.__dao.load_attendee_events(const.GOOD_USER_ID)
        self.assertTrue(len(val) == 1)
        self.assertTrue('id' in val[0])
        self.assertTrue('name' in val[0])
        self.assertTrue('creator_id' in val[0])
        self.assertTrue('created_date' in val[0])

        # test exception handeling
        builtins.db_fail = 'True'
        try:
            val = self.__dao.load_attendee_events(const.GOOD_USER_ID)
        except Exception as e:
            self.assertTrue(isinstance(e, DaoException))

    def save_event_test (self):
        # test normal functionality
        builtins.db_return_object = [
            ['name'],
            None,
            None,
            ['idk', 'some name', 'someCreator', 'someCreatorId'],
            None,
            [['abcd1234']]
        ]
        val = self.__dao.save_event({
            'name': 'Some cool thing',
            'creator_id': 'lololo'
        })
        self.assertTrue('id' in val)
        self.assertTrue('name' in val)
        self.assertTrue('creator_id' in val)
        self.assertTrue('created_date' in val)

        # test unable to generate unique id
        builtins.db_return_object = [
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
