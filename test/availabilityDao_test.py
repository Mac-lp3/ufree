import os
import unittest
import builtins
from classes.dao.AvailabilityDao import AvailabilityDao
from classes.exception.DaoException import DaoException

class AvailabilityDaoTest(unittest.TestCase):

    def setUp (self):
        builtins.db_fail = os.environ['TEST_DB_FAIL']
        self.__dao = AvailabilityDao()
        self.availability_object = {
            'id': 1234,
            'attendee_id': 2345,
            'event_id': 'lskdajfh234a231hlsadf234',
            'year': '2017',
            'january': '00000000000000000000000000',
            'february': '00000000000000000000000000',
            'march': '00000000000000000000000000',
            'april': '00000000000000000000000000',
            'may': '00000000000000000000000000',
            'june': '00000000000000000000000000',
            'july': '00000000000000000000000000',
            'august': '00000000000000000000000000',
            'september': '00000000000000000000000000',
            'october': '00000000000000000000000000',
            'november': '00000000000000000000000000',
            'december': '00000000000000000000000000'
        }
        self.return_row = [
            1234,
            2345,
            'lskdajfh234a231hlsadf234',
            '2017',
            'january',
            'february',
            'march',
            'april',
            'may',
            'june',
            'july',
            'august',
            'september',
            'october',
            'november',
            'december'
        ]

    def delete_availability_test (self):
        try:
            self.__dao.delete_availability()
            self.__dao.delete_availability(availability_id=1234)
            self.__dao.delete_availability(event_id='jkh234kjlh1234')
            self.__dao.delete_availability(attendee_id=2341)
            self.__dao.delete_availability(
                attendee_id=2341, event_id='jkh234kjlh1234'
            )
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)

    def update_availability_test (self):
        # test normal behavior
        builtins.return_pattern = [self.return_row]
        obj = self.__dao.update_availability(self.availability_object)
        self.assertTrue('id' in obj)
        self.assertTrue('february' in obj)
        self.assertTrue('august' in obj)
        self.assertTrue('december' in obj)

        # test exception handeling
        builtins.db_fail = 'True'
        try:
            val = self.__dao.update_availability(self.availability_object)
        except Exception as e:
            self.assertTrue(isinstance(e, DaoException))
        builtins.db_fail = 'False'

    def get_availability_test (self):
        # test attendee_id input
        builtins.return_pattern = [self.return_row]
        obj = self.__dao.get_availability(attendee_id=2345)
        self.assertTrue('id' in obj)
        self.assertTrue('february' in obj)
        self.assertTrue('august' in obj)
        self.assertTrue('december' in obj)

        # test event_id input
        builtins.return_pattern = [self.return_row]
        obj = self.__dao.get_availability(event_id=1234)
        self.assertTrue('id' in obj)
        self.assertTrue('february' in obj)
        self.assertTrue('august' in obj)
        self.assertTrue('december' in obj)

        # test event_id and attendee_id input
        builtins.return_pattern = [self.return_row]
        obj = self.__dao.get_availability(event_id=1234, attendee_id=2345)
        self.assertTrue('id' in obj)
        self.assertTrue('february' in obj)
        self.assertTrue('august' in obj)
        self.assertTrue('december' in obj)

        # test exception handeling
        builtins.db_fail = 'True'
        try:
            val = self.__dao.get_availability(event_id=1234)
        except Exception as e:
            self.assertTrue(isinstance(e, DaoException))
        builtins.db_fail = 'False'

if __name__ == '__main__':
    unittest.main()
