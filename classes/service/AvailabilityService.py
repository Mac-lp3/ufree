import os
import sys
import json
import inspect
import importlib
from pyramid.response import Response
from classes.provider.DependencyProvider import DependencyProvider
from classes.util.HashCodeUtils import HashCodeUtils
from classes.util.EventValidator import EventValidator
from classes.util.AttendeeValidator import AttendeeValidator
from classes.exception.ServiceException import ServiceException
from classes.exception.BaseAppException import BaseAppException

class AvailabilityService:

    def __init__ (self):
        # init DAOs based on environment
        self.__provider = DependencyProvider()
        self.__event_dao = self.__provider.get_instance('EventDao')
        self.__attendee_dao = self.__provider.get_instance('AttendeeDao')
        self.__availability_dao = self.__provider.get_instance('AvailabilityDao')
        self.__eventValidator = EventValidator()
        self.__attendeeValidator = AttendeeValidator()

    # get all availability obs for this event
    def get_event_availability (self, req):
        try:
            event_id = req.matchdict['eventId']
            self.__eventValidator.validate_event_id(event_id)

            data = self.__availability_dao.get_event_availability(event_id)
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while loading availability for event:',
                event_id
            )
        return response

    # delete all availability obs for this event
    def delete_event_availability (self, req):
        try:
            event_id = req.matchdict['eventId']
            self.__eventValidator.validate_event_id(event_id)

            self.__availability_dao.delete_event_availability(event_id)
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while deleting availability for event:',
                event_id
            )
        return response

    # get all availability obs for this attendee
    def get_attendee_availability (self, req):
        try:
            event_id = req.matchdict['eventId']
            self.__eventValidator.validate_event_id(event_id)

            attendee_id = req.matchdict['attendeeId']
            self.__attendeeValidator.validate_attendee_id(attendee_id)

            data = self.__availability_dao.get_attendee_availability(
                event_id,
                attendee_id
            )
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while loading availability for attendee:',
                attendee_id
            )

        return response

    # get availability ob for this attendee
    def get_availability (self, req):
        try:
            availability_id = req.matchdict['availabilityId']
            # TODO add vaildator
            #self.__attendeeValidator.validate_attendee_id(availability_id)

            data = self.__availability_dao.get_availability(attendee_id)
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while loading availability with id:',
                availability_id
            )

        return response

    # add availability ob for this attendee

    # update availability ob for this attendee

    # delte availability ob for this attendee
    def delete_attendee_availability (self, req):
        # TODO should accept event ID too?
        try:
            attendee_id = req.matchdict['attendeeId']
            self.__attendeeValidator.validate_attendee_id(attendee_id)

            self.__availability_dao.delete_attendee_availability(attendee_id)
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while deleting attendee availability:',
                availability_id
            )

        return response

    # delete all availability obs for this attendee
