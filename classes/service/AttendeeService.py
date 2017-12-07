import os
import sys
import json
import inspect
import importlib
from pyramid.response import Response
from classes.util.HashCodeUtils import HashCodeUtils
from classes.util.EventValidator import EventValidator
from classes.util.AttendeeValidator import AttendeeValidator
from classes.exception.ServiceException import ServiceException
from classes.exception.BaseAppException import BaseAppException
from classes.provider.dependency_provider import DependencyProvider

class AttendeeService:

    def __init__ (self):
        # init DAOs based on environment
        self.__provider = DependencyProvider()
        self.__event_dao = self.__provider.get_instance('EventDao')
        self.__attendee_dao = self.__provider.get_instance('AttendeeDao')
        self.__availability_dao = self.__provider.get_instance('AvailabilityDao')
        self.__eventValidator = EventValidator()
        self.__attendeeValidator = AttendeeValidator()

    def load_attendee (self, req):
        '''
        returns JSON data of this single attendee
        '''
        try:
            # validate
            att_id = req.matchdict['attendee_id']
            if att_id is None:
                raise ServiceException('Id was not found on this request')

            self.__attendeeValidator.validate_attendee_id(
                att_id
            )
            data = self.__attendee_dao.load_attendee(att_id)
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while loading attendee with id',
                att_id
            )
        return response

    def update_attendee (self, req):
        '''
        Updates an attendee's details such as name or email address
        '''
        try:
            if 'id' not in req.json_body:
                raise ServiceException('Id was not found on this request')
            self.__attendeeValidator.validate_attendee_request(req)
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
        '''
        TODO ?
        Updates the availability of an attendee
        '''
        try:
            # TODO validate availability
            self.__attendeeValidator.validate_attendee_request(req)
            data = self.__availability_dao.update_availability(req.json_body)
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

    def load_event_attendees (self, req):
        '''
        Returns a JSON list of all attendees in this event
        '''
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

    def create_attendee (self, req):
        '''
        Create and attendee and join the target event.
        '''
        try:
            # validate event ID and attendee payload
            eventId = req.matchdict['eventId']
            self.__eventValidator.validate_event_id(eventId)
            self.__attendeeValidator.validate_attendee_request(req)

            # create the attendee and join the event
            data = self.__attendee_dao.save_attendee(req.json_body)
            self.__attendee_dao.join_event(data['id'], eventId)

            # build the response body
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)

        except BaseAppException as e:
            raise ServiceException(str(e))

        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException('An error occurred while creating this event.')

        return response

    def remove_attendee_from_event (self, req):
        try:
            att_id = req.json_body['id']
            event_id = req.matchdict['eventId']
            self.__attendeeValidator.validate_attendee_id(att_id)
            self.__eventValidator.validate_event_id(event_id)
            data = self.__attendee_dao.delete_attendee(att_id, event_id)

        except BaseAppException as e:
            raise ServiceException(str(e))

        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException('An error occurred while creating this event.')

        return Response(status=200)

    def add_attendee_to_event (self, req):
        try:
            self.__attendeeValidator.validate_attendee_request(req)
            data = self.__attendee_dao.join_event(
                req.json_body['id'],
                req.matchdict['eventId']
            )

        except BaseAppException as e:
            raise ServiceException(str(e))

        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException('An error occurred while creating this event.')

        return Response(status=200)
