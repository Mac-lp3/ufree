import re
import datetime
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

        # init validation patterns
        self.__availability_id_pattern = r'^[\w\d\s-]+$'
        self.__year_pattern = r'2[0-9]{3}'
        self.__january_pattern = r'[0-3]{31}'
        self.__february_pattern = r'[0-3]{28}'
        self.__february_leap_pattern = r'[0-3]{29}'
        self.__march_pattern = r'[0-3]{31}'
        self.__april_pattern = r'[0-3]{30}'
        self.__may_pattern = r'[0-3]{31}'
        self.__june_pattern = r'[0-3]{30}'
        self.__july_pattern = r'[0-3]{31}'
        self.__august_pattern = r'[0-3]{31}'
        self.__september_pattern = r'[0-3]{30}'
        self.__october_pattern = r'[0-3]{31}'
        self.__november_pattern = r'[0-3]{30}'
        self.__december_pattern = r'[0-3]{31}'

        # define general error
        self.__empty_value_message = '{0} is blank. A value for {0} is required.'

    def vaildaite_availability_request (self, req):
        '''
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
        '''
        error_messages = []
        try:
            # if POST or PUT validate the ID
            if (req.method === 'POST' || req.method === 'PUT'):
                av_id = req.matchdict['availabilityId']
                if av_id:
                    validate_availability_id(av_id)
                else:
                    error_messages.append(
                        self.__empty_value_message.format('availabilityId')
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
            if 'year' in req.json_body:
                self.validate_field(
                    self.__year_pattern,
                    req.json_body['year']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('year')
                )

            # validate january
            if 'january' in req.json_body:
                self.validate_field(
                    self.__january_pattern,
                    req.json_body['january']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('january')
                )

            # validate february
            if 'february' in req.json_body:
                self.validate_field(
                    self.__february_pattern,
                    req.json_body['february']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('february')
                )

            # validate march
            if 'march' in req.json_body:
                self.validate_field(
                    self.__march_pattern,
                    req.json_body['march']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('march')
                )

            # validate april
            if 'april' in req.json_body:
                self.validate_field(
                    self.__april_pattern,
                    req.json_body['april']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('april')
                )

            # validate may
            if 'may' in req.json_body:
                self.validate_field(
                    self.__may_pattern,
                    req.json_body['may']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('may')
                )

            # validate june
            if 'june' in req.json_body:
                self.validate_field(
                    self.__june_pattern,
                    req.json_body['june']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('june')
                )

            # validate july
            if 'july' in req.json_body:
                self.validate_field(
                    self.__july_pattern,
                    req.json_body['july']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('july')
                )

            # validate august
            if 'august' in req.json_body:
                self.validate_field(
                    self.__august_pattern,
                    req.json_body['august']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('august')
                )

            # validate september
            if 'september' in req.json_body:
                self.validate_field(
                    self.__september_pattern,
                    req.json_body['september']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('september')
                )

            # validate october
            if 'october' in req.json_body:
                self.validate_field(
                    self.__october_pattern,
                    req.json_body['october']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('october')
                )

            # validate november
            if 'november' in req.json_body:
                self.validate_field(
                    self.__november_pattern,
                    req.json_body['november']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('november')
                )

            # validate december
            if 'december' in req.json_body:
                self.validate_field(
                    self.__december_pattern,
                    req.json_body['december']
                )
            else:
                error_messages.append(
                    self.__empty_value_message.format('december')
                )

        except ValidationException as e:
            error_messages.append(e.messages)

        if error_messages:
            raise ValidationException(error_messages)

        return None

    def validate_field (self, pattern, value):
        '''
        Generic method for regex field validation
        '''
        error_messages = []
        if isinstance(value, str):
            test = re.search(pattern, value)
            if test == None or test.string != value:
                error_messages.append(
                    'Field failed validation;', value
                )
        else:
            error_messages.append('Fields must all be strings')

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
