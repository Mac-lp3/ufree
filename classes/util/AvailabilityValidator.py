import re
import datetime
from classes.exception.ValidationException import ValidationException

class AvailabilityValidator:

    # just letters and numbers
    __availability_id_pattern = r'^[\w\d\s-]+$'

    def vaildaite_availability_request (self, req):
        pass

    def validate_availability_id (self, availability_id):
        error_messages = []
        # Validate ID field
        if isinstance(availability_id, str):
            test = re.search(
                self.__availability_id_pattern,
                availability_id
            )
            if test == None or test.string != availability_id:
                error_messages.append(
                    'ID must only contain letters or numbers'
                )
        else:
            error_messages.append('Availability ID must be a String')

        if error_messages:
            raise ValidationException(error_messages)
