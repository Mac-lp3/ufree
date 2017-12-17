import re
import datetime
from classes.util.HashCodeUtils import HashCodeUtils
from classes.exception.validation_exception import ValidationException

class EventValidator:

    #just letters, numbers, and spaces
    __event_name_pattern = r'^[\w\d\s-]+$'
    __event_name_length = 50
    __event_creator_pattern = r'^[\w\d\s-]+$'
    __event_creator_length = 25

    def validate_event_id (self, event_id):
        error_messages = HashCodeUtils.validate_hash(event_id)
        if error_messages:
            raise ValidationException(error_messages)
        return None

    def validate_event(self, eventObject):
        '''
        Validates each field of the event object.

        Returns a list of error messages or an empty list if none found.
        '''

        error_messages = []

        # Validate name field
        if 'name' in eventObject:
            if not isinstance(eventObject['name'], str):
                error_messages.append('Name must be a string')

            elif len(eventObject['name']) > self.__event_name_length:
                message = 'Name must be less than {0} characters'.format(
                    self.__event_name_length
                )
                error_messages.append(message)

            else:
                test = re.search(self.__event_creator_pattern, eventObject['name'])
                if test == None or test.string != eventObject['name']:
                    error_messages.append(
                        'Name must only contain letters, numbers, spaces, or dashes'
                    )
        else:
            error_messages.append('Name is blank. A value for name is required')

        # Validate creator field
        if 'creator' in eventObject:

            if not isinstance(eventObject['creator'], str):
                error_messages.append('Creator must be a string')

            elif len(eventObject['creator']) > self.__event_creator_length:
                message = 'Creator must be less than {0} characters'.format(
                    self.__event_creator_length
                )
                error_messages.append(message)

            else:
                test = re.search(self.__event_creator_pattern, eventObject['creator'])
                if test == None or test.string != eventObject['creator']:
                    error_messages.append(
                        'Creator must only contain letters, numbers, spaces, or dashes'
                    )
        else:
            error_messages.append('Creator is blank. A value for creator is required')

        if error_messages:
            raise ValidationException(error_messages)

        return None
