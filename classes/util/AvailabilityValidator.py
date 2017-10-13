import re
import datetime
from classes.util.EventValidator import EventValidator
from classes.util.AttendeeValidator import AttendeeValidator
from classes.provider.DependencyProvider import DependencyProvider
from classes.exception.ValidationException import ValidationException

class AvailabilityValidator:

    def __init__ (self):
        # init DAOs based on environment
        self.__provider = DependencyProvider()
        self.__event_dao = self.__provider.get_instance('EventDao')
        self.__attendee_dao = self.__provider.get_instance('AttendeeDao')
        self.__availability_dao = self.__provider.get_instance('AvailabilityDao')

        # init other validators
        self.__event_validator = EventValidator()
        self.__attendee_validator = AttendeeValidator()

        # init field validation info
        self.__availability_id_pattern = r'^[\w\d\s-]+$'
        self.__id_field = {
            'name': 'id',
            'pattern': r'^[\w\d\s-]+$',
            'error_message': 'ID field must contain only numbers or letters.'
        }
        self.__year_field = {
            'name': 'year',
            'pattern': r'2[0-9]{3}',
            'error_message': 'Year must start with 2 and be 4 digits long.'
        }
        base_err_string = (
            '{0} field must have length {1} and only contain 0-3.'
        )
        self.__january_field = {
            'name': 'january',
            'pattern': r'[0-3]{31}',
            'error_message': base_err_string.format('January', 31)
        }
        self.__february_field = {
            'name': 'february',
            'pattern': r'[0-3]{28}',
            'error_message': base_err_string.format('February', 28)
        }
        self.__february_leap_field = {
            'name': 'february',
            'pattern': r'[0-3]{29}',
            'error_message': 'On leap years, Feburary must be 2 characters and only contain values 0-3'
        }
        self.__march_field = {
            'name': 'march',
            'pattern': r'[0-3]{31}',
            'error_message': base_err_string.format('March', 31)
        }
        self.__april_field = {
            'name': 'april',
            'pattern': r'[0-3]{30}',
            'error_message': base_err_string.format('April', 30)
        }
        self.__may_field = {
            'name': 'may',
            'pattern': r'[0-3]{31}',
            'error_message': base_err_string.format('May', 31)
        }
        self.__june_field = {
            'name': 'june',
            'pattern': r'[0-3]{30}',
            'error_message': base_err_string.format('June', 30)
        }
        self.__july_field = {
            'name': 'july',
            'pattern': r'[0-3]{31}',
            'error_message': base_err_string.format('July', 31)
        }
        self.__august_field = {
            'name': 'august',
            'pattern': r'[0-3]{31}',
            'error_message': base_err_string.format('August', 31)
        }
        self.__september_field = {
            'name': 'september',
            'pattern': r'[0-3]{30}',
            'error_message': base_err_string.format('September', 30)
        }
        self.__october_field = {
            'name': 'october',
            'pattern': r'[0-3]{31}',
            'error_message': base_err_string.format('October', 31)
        }
        self.__november_field = {
            'name': 'novomber',
            'pattern': r'[0-3]{30}',
            'error_message': base_err_string.format('November', 30)
        }
        self.__december_field = {
            'name': 'december',
            'pattern': r'[0-3]{31}',
            'error_message': base_err_string.format('December', 31)
        }

        # define general error
        self.__empty_value_message = '{0} is blank. A value for {0} is required.'

    def validate_availability_request (self, req):
        error_messages = []
        try:
            # if POST or PUT validate the ID
            if (req.method == 'POST' or req.method == 'PUT'):
                av_id = req.matchdict['availability_id']
                if av_id:
                    self.validate_availability_id(av_id)
                else:
                    error_messages.append(
                        self.__empty_value_message.format('availability_id')
                    )

            # validate attendee id
            if 'attendee_id' in req.json_body:
                self.__attendee_validator.validate_attendee_id(
                    req.json_body['attendee_id']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('attendee_id')
                )

            # validate event ID
            if 'event_id' in req.json_body:
                self.__event_validator.validate_event_id(
                    req.json_body['event_id']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('event_id')
                )

            # validate year
            self.validate_field(
                self.__year_field,
                req.json_body['year']
            )

            # validate january
            self.validate_field(
                self.__january_field,
                req.json_body['january']
            )

            # validate february
            self.validate_field(
                self.__february_field,
                req.json_body['february']
            )

            # validate march
            self.validate_field(
                self.__march_field,
                req.json_body['march']
            )

            # validate april
            self.validate_field(
                self.__april_field,
                req.json_body['april']
            )

            # validate may
            self.validate_field(
                self.__may_field,
                req.json_body['may']
            )

            # validate june
            self.validate_field(
                self.__june_field,
                req.json_body['june']
            )

            # validate july
            self.validate_field(
                self.__july_field,
                req.json_body['july']
            )

            # validate august
            self.validate_field(
                self.__august_field,
                req.json_body['august']
            )

            # validate september
            self.validate_field(
                self.__september_field,
                req.json_body['september']
            )

            # validate october
            self.validate_field(
                self.__october_field,
                req.json_body['october']
            )

            # validate november
            self.validate_field(
                self.__november_field,
                req.json_body['november']
            )

            # validate december
            self.validate_field(
                self.__december_field,
                req.json_body['december']
            )

        except ValidationException as e:
            error_messages.append(e.messages)
        except Exception as e:
            print('Exception during request validation:', e)
            raise ValidationException(
                'An error has occurred. Please try again later.'
            )
        if error_messages:
            raise ValidationException(error_messages)

        return None

    def validate_field (self, field, value):
        '''
        Generic method for regex field validation
        '''
        error_messages = []
        try:
            if isinstance(value, str):
                test = re.search(field['pattern'], value)
                if test == None or test.string != value:
                    error_messages.append(
                        field['error_message']
                    )
            else:
                error_messages.append(
                        'Field {0} must all be a non-empty string'.format(
                            field['name']
                        )
                    )
        except Exception as e:
            print('Error occurred while validating field:', e, field)
        if error_messages:
            raise ValidationException(error_messages)


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
