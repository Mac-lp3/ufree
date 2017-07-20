import os
import importlib
from classes.util.AttendeeValidator import AttendeeValidator
from classes.dao.AttendeeDao import AttendeeDao
from classes.exception.ValidationException import ValidationException

class UserFilter():

    def __init__ (self):
        # init DAO based on environment
        self.__inputValidator = AttendeeValidator()
        if os.environ['ENV'] == 'test':
            temp = importlib.import_module('test.classes.AttendeeDao')
            self.__attendee_dao = temp.AttendeeDao()
        else:
            temp = importlib.import_module('classes.dao.AttendeeDao')
            self.__attendee_dao = temp.AttendeeDao()

    def __create_new_user (self, req_body):
        # Get the creator or attendee name.
        attendee_name = ''
        if 'creator' in req_body['payload']:
            attendee_name = req_body['payload']['creator']
        elif 'name' in req_body['payload']:
            attendee_name = req_body['payload']['name']

        # If neither is found, then this is a bad request
        if not attendee_name:
            raise ValidationException(
                'Name for this user could not be located'
            )

        # create a new user with the provided name
        self.__inputValidator.validate_attendee_name(attendee_name)
        att = self.__attendee_dao.save_attendee({
            'name': attendee_name
        })

        # return the attendee object
        return att

    def set_user_id (self, req):
        '''
        Checks if user_id cookie is in the request. Creates a new user if not.
        '''

        # check if cookies were sent with this request
        if 'cookies' in req and 'user_id' in req['cookies']:
            cookies = req_body['cookies']
            # Check if user_id cookie was sent with the request
            if cookies['user_id']:
                # validate the ID
                self.__inputValidator.validate_attendee_id(cookies['user_id'])
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
                req.cookies.push({
                    'user_id': att['id']
                })
                return req
        # if not, create a new user and assign user_id cookie
        else:
            att = self.__create_new_user(req.json_body)
            req.cookies = []
            req.cookies['user_id'] = att['id']
            return req
