import os
import builtins
from classes.exception.dao_exception import DaoException

class AvailabilityDao:

    __simple_obj = {
        'id': '1234',
        'attendee_id': '123345',
        'event_id': 'asdf876asfd786af',
        'year': '2017',
        'january': '000000000000000000000000000000',
        'february': '000000000000000000000000000000',
        'march': '000000000000000000000000000000',
        'april': '000000000000000000000000000000',
        'may': '000000000000000000000000000000',
        'june': '000000000000000000000000000000',
        'july': '000000000000000000000000000000',
        'august': '000000000000000000000000000000',
        'september': '000000000000000000000000000000',
        'october': '000000000000000000000000000000',
        'november': '000000000000000000000000000000',
        'december': '000000000000000000000000000000'
    }

    def get_availability (self, attendee_id='', event_id=''):
        if builtins.db_fail == 'True':
            raise DaoException('General exception')
        return self.__simple_obj

    def update_availability (self, availability):
        if builtins.db_fail == 'True':
            raise DaoException('General exception')
        return self.__simple_obj

    def delete_availability (self, availability_id='', attendee_id='', event_id=''):
        if builtins.db_fail == 'True':
            raise DaoException('General exception')
        pass

    def create_availability(self, availability):
        if builtins.db_fail == 'True':
            raise DaoException('General exception')
        return self.__simple_obj

    def availability_exists (self, event_id, attendee_id, year):
        if builtins.db_fail == 'True':
            raise DaoException('General exception')
        return True
