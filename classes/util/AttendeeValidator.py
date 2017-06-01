import re
import datetime
from classes.exception.ValidationException import ValidationException

class AttendeeValidator:

    # just letters, numbers, and spaces
    __attendee_name_pattern = r'^[\w\d\s-]+$'
    __attendee_name_length = 20

    def validate_attendee (self, attendee):
        error_messages = []
        try:
            self.validate_attendee_name(attendee['name'])
        except ValidationException as e:
            error_messages.append(e.messages)

        try:
            self.validate_attendee_id(attendee['id'])
        except ValidationException as e:
            error_messages.append(e.messages)

        if error_messages:
            raise ValidationException(error_messages)

        return None

    def validate_attendee_name (self, name):
        error_messages = []
        if 'name' in attendee:
            if not isinstance(attendee['name'], str):
                error_messages.append('Name must be a string')

            elif len(attendee['name']) > self.__attendee_name_length:
                message = 'Name must be less than {0} characters'.format(
                    self.__attendee_name_length
                )
                error_messages.append(message)

            else:
                test = re.search(self.__attendee_name_pattern, attendee['name'])
                if test == None or test.string != attendee['name']:
                    error_messages.append(
                        'Name must only contain letters, numbers, spaces, or dashes'
                    )
        else:
            error_messages.append('Name is blank. A value for name is required')

        if error_messages:
            raise ValidationException(error_messages)

    def validate_attendee_id (self, id):
        error_messages = []
        # Validate ID field
        if 'id' in attendee:
            try:
                int(attendee['id'])
            except Exception:
                error_messages.append('Attendee ID must be an integer')
        else:
                error_messages.append('Attendee ID must not be blank')

        if error_messages:
            raise ValidationException(error_messages)
