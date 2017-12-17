import os
import importlib
from classes.dao.attendee_dao import AttendeeDao
from classes.util.AttendeeValidator import AttendeeValidator
from classes.provider.dependency_provider import DependencyProvider
from classes.exception.ValidationException import ValidationException

class UserFilter():

    def __init__ (self):
        # retrieve dependencies based on environment
        self.__provider = DependencyProvider()
        self.__attendee_dao = self.__provider.get_instance('AttendeeDao')
        self.__attendeeValidator = AttendeeValidator()

    def __create_new_user (self, req_body):
        attendee_name = ''
        try:
            if 'creator' in req_body:
                attendee_name = req_body['creator']
            elif 'name' in req_body:
                attendee_name = req_body['name']
        except Exception as e:
            raise ValidationException(
                'Payload was not found in this request'
            )
        else:
            if not attendee_name:
                raise ValidationException(
                    'Name for this user could not be located'
                )

        # create a new user with the provided name
        self.__attendeeValidator.validate_attendee_name(attendee_name)
        att = self.__attendee_dao.save_attendee({
            'name': attendee_name
        })

        # return the attendee object
        return att

    def set_user_id (self, req):
        '''
        Checks if user_id cookie is in the request. Creates a new user if not.
        '''

        try:
            # check if cookies were sent with this request
            cookies = req.req_body['cookies']

            # Check if user_id cookie was sent with the request
            if cookies['user_id']:
                # validate the ID
                self.__attendeeValidator.validate_attendee_id(cookies['user_id'])
                # if the id exists in the DB, return the request unchanged
                if self.__attendee_dao.attendee_exists(cookies['user_id']):
                    return req
                else:
                    # ID not in database. Create new user and overwrite cookie
                    att = self.__create_new_user(req.json_body)
                    req.cookies['user_id'] = att['id']
                    return req
            else:
                # if not, create new user and attach user_id cookie
                att = self.__create_new_user(req.json_body)
                req.cookies['user_id'] = att['id']

        except Exception as e:
            # if not, create new user and attach user_id cookie
            att = self.__create_new_user(req.json_body)
            req.cookies['user_id'] = att['id']
            return req
