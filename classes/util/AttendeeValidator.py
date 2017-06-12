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
            if 'name' in attendee:
                self.validate_attendee_name(attendee['name'])
            else:
                error_messages.append(
                    'Name is blank. A value for name is required'
                )
        except ValidationException as e:
            error_messages.append(e.messages)

        try:
            if 'id' in attendee:
                self.validate_attendee_id(attendee['id'])
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
        if 'id' in attendee:
            try:
                int(attendee['id'])
            except Exception:
                error_messages.append('Attendee ID must be an integer')
        else:
            error_messages.append('Attendee ID must not be blank')

        if error_messages:
            raise ValidationException(error_messages)
