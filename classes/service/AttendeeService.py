import os
import sys
import json
import inspect
import importlib
from classes.util.HashCodeUtils import HashCodeUtils
from classes.util.EventValidator import EventValidator
from classes.util.AttendeeValidator import AttendeeValidator
from classes.exception.ServiceException import ServiceException
from classes.exception.BaseAppException import BaseAppException
from classes.provider.DependencyProvider import DependencyProvider

class AttendeeService:

    def __init__ (self):
        # init DAOs based on environment
        self.__provider = DependencyProdiver()
        self.__event_dao = self.__provider.get_instance('EventDao')
        self.__attendee_dao = self.__provider.get_instance('AttendeeDao')
        self.__availability_dao = self.__provider.get_instance('AvailabilityDao')
        self.__eventValidator = EventValidator()
        self.__attendeeValidator = AttendeeValidator()

    def load_attendee (self, request):
        pass

    def update_attendee (self, request):
        response_body = {}
        try:
            if 'id' not in req.json_body:
                raise ServiceException('Id was not found on this request')
            inputErrors = self.__attendeeValidator.validate_attendee_request(req)
            data = self.__attendee_dao.update_attendee(req.json_body)
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)

        except BaseAppException as e:
            # Handle DAO/Validation errors
            raise ServiceException(str(e))
        except Exception as e:
            # Handle unexpected errors
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while updating your info.'
            )

        return response

    def update_attendee_availability (self, req):
        req_body = req.json_body
        response_body = {}
        try:
            # TODO validate availability
            #inputErrors = self.__eventValidator.validate_attendee(req_body)
            data = self.__availability_dao.update_availability(req_body)
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)
        except BaseAppException as e:
            # Handle DAO/Validation errors
            raise ServiceException(str(e))
        except Exception as e:
            # Handle unexpected errors
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while updating availability.'
            )
        return response

    def get_event_attendees (self, req):
        try:
            # validate the event id
            eventId = req.matchdict['eventId']
            self.__eventValidator.validate_event_id(eventId)

            # load the attendee list
            data = self.__attendee_dao.load_event_attendees(eventId)

            # build response object
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)

        except BaseAppException as e:
            # Handle DAO/Validation errors
            raise ServiceException(str(e))
        except Exception as e:
            # Handle unexpected errors
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while retrieving attendee list.'
            )

        return response

    def create_attendee (self, request):
        pass

    def remove_attendee_from_event (self, request):
        pass

    def add_attendee_to_event (self, request):
        pass
