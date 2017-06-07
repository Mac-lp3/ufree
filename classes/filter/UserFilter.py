from classes.util.AttendeeDao import AttendeeValidator
from classes.dao.AttendeeDao import AttendeeDao
from classes.exception.ValidationException import ValidationException
def UserFilter():

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
        if 'cookies' in req_body and 'user_id' in req_body['cookies']:
            # throws exception on failure
            cookies = req_body['cookies']
            if cookies['user_id']:
                self.__inputValidator.validate_attendee_id(cookies['user_id'])
                if self.__attendee_dao.attendee_exists(cookies['user_id']):
                    # user exists and cookie is not stale
                    return req
                else:
                    # stale cookie. create new user and overwrite existing cookie
                    att = self.__create_new_user(req.json_body)
                    req.cookies['user_id'] = att['id']
                    return req
            else:
                # create new user and cookie
                att = self.__create_new_user(req.json_body)
                req.cookies.push({
                    'user_id': att['id']
                })
                return req
        else:
            att = self.__create_new_user(req.json_body)
            req.cookies = []
            req.cookies['user_id'] = att['id']
            return req
