import os
import unittest
import builtins
from classes.dao.AvailabilityDao import AvailabilityDao
from classes.exception.DaoException import DaoException

class AvailabilityDaoTest(unittest.TestCase):

    def setUp (self):
        builtins.db_fail = os.environ['TEST_DB_FAIL']
        self.__dao = AvailabilityDao()

    def get_availability_test (self):
        # test attendee_id input
        builtins.return_pattern = [
            [
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
        ]
        obj = self.__dao.get_availability(attendee_id=2345)
        self.assertTrue('id' in obj)
        self.assertTrue('february' in obj)
        self.assertTrue('august' in obj)
        self.assertTrue('december' in obj)

        # test event_id input
        builtins.return_pattern = [
            [
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
        ]
        obj = self.__dao.get_availability(event_id=1234)
        self.assertTrue('id' in obj)
        self.assertTrue('february' in obj)
        self.assertTrue('august' in obj)
        self.assertTrue('december' in obj)

        # test event_id and attendee_id input
        builtins.return_pattern = [
            [
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
        ]
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
