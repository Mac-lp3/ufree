import re
import datetime
from classes.exception.validation_exception import ValidationException

class AttendeeValidator:

    # just letters, numbers, and spaces
    __attendee_id_pattern = r'^[\w\d\s-]+$'
    __attendee_name_pattern = r'^[\w\d\s-]+$'
    __attendee_name_length = 30

    def validate_attendee_request (self, req):
        error_messages = []
        try:
            if 'name' in req.json_body:
                self.validate_attendee_name(req.json_body['name'])
            else:
                error_messages.append(
                    'Name is blank. A value for name is required'
                )
        except ValidationException as e:
            error_messages.append(e.messages)

        try:
            if 'id' in req.json_body:
                self.validate_attendee_id(req.json_body['id'])
            elif 'user_id' in req.cookies:
                self.validate_attendee_id(req.cookies['user_id'])
            else:
                error_messages.append(
                    'A suitable ID could not be found for this request'
                )
        except ValidationException as e:
            error_messages.append(e.messages)

        if error_messages:
            raise ValidationException(error_messages)

        return None

    def validate_attendee_name (self, name):
        error_messages = []

        if not isinstance(name, str):
            error_messages.append('Name must be a string')

        elif len(name) > self.__attendee_name_length:
            message = 'Name must be less than {0} characters'.format(
                self.__attendee_name_length
            )
            error_messages.append(message)

        else:
            test = re.search(self.__attendee_name_pattern, name)
            if test == None or test.string != name:
                error_messages.append(
                    'Name must only contain letters, numbers, spaces, or dashes'
                )

        if error_messages:
            raise ValidationException(error_messages)

    def validate_attendee_id (self, id):
        error_messages = []
        # Validate ID field
        if isinstance(id, str):
            test = re.search(self.__attendee_id_pattern, id)
            if test == None or test.string != id:
                error_messages.append(
                    'ID must only contain letters or numbers'
                )
        else:
            error_messages.append('Attendee ID must be a String')

        if error_messages:
            raise ValidationException(error_messages)
