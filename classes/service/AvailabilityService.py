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

        # get all availability obs for this attendee

        # get availability ob for this attendee

        # add availability ob for this attendee

        # update availability ob for this attendee

        # delte availability ob for this attendee

        # delete all availability obs for this attendee
