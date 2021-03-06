import os
import sys
import json
import inspect
import importlib
from pyramid.response import Response
from classes.provider.dependency_provider import DependencyProvider
from classes.util.event_validator import EventValidator
from classes.util.attendee_validator import AttendeeValidator
from classes.exception.service_exception import ServiceException
from classes.exception.base_app_exception import BaseAppException

class EventService:

    def __init__ (self):
        # init DAOs based on environment
        self.__provider = DependencyProvider()
        self.__event_dao = self.__provider.get_instance('EventDao')
        self.__attendee_dao = self.__provider.get_instance('AttendeeDao')
        self.__availability_dao = self.__provider.get_instance('AvailabilityDao')
        self.__eventValidator = EventValidator()
        self.__attendeeValidator = AttendeeValidator()

    def load_event (self, req):
        try:
            # validate
            eventId = req.matchdict['eventId']
            self.__eventValidator.validate_event_id(eventId)
            data = self.__event_dao.load_event(eventId)
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while loading this event.'
            )
        return response

    def update_event (self, req):
        try:
            payload = req.json_body
            self.__eventValidator.validate_event(payload)
            data = self.__event_dao.update_event(payload)
            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = json.dumps(data)
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while updating this event.'
            )
        return response

    def create_event (self, req):
        '''
        Creates a new event.

        Validates the request object, extracts all required information, and
        builds the event and associated objects.
        '''
        # TODO year mechanism.
        try:
            inputErrors = self.__eventValidator.validate_event(req.json_body)
            response_body = {}
            if not inputErrors:
                # set the creator_id and save the event
                req.json_body['creator_id'] = req.cookies['user_id']
                data = self.__event_dao.save_event(req.json_body)

                # build the response body
                response_body = json.dumps(data)

            else:
                response_body = json.dumps(inputErrors)

            response = Response(content_type='application/json', status=200)
            response.charset = 'UTF-8'
            response.json_body = response_body

        except BaseAppException as e:
            raise ServiceException(str(e))

        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException('An error occurred while creating this event.')

        return response

    def delete_event (self, req):
        try:
            # validate event ID
            eventId = req.matchdict['eventId']
            inputErrors = self.__eventValidator.validate_event_id(eventId)

            # make sure this user is the creator
            user_id = req.cookies['user_id']
            event = self.__event_dao.load_event(eventId)

            # delete event if so
            if event['creator_id'] == user_id:
                self.__event_dao.delete_event(eventId)
            else:
                raise ServiceException(
                    'Only the creator cannot delete this event'
                )
        except BaseAppException as e:
            raise ServiceException(str(e))

        return Response(status=200)

    def delete_event_attendee (self, req):
        try:
            eventId = req.matchdict['eventId']
            attendee_id = req.matchdict['attendee_id']
            self.__eventValidator.validate_event_id(eventId)
            self.__attendeeValidator.validate_attendee_id(attendee_id)

            if req.cookies['user_id'] == attendee_id:
                # user is leaving this event
                self.__attendee_dao.leave_event(attendee_id, eventId)
            else:
                # check if this is the event creator
                event = self.__event_dao.load_event(eventId)
                if req.cookies['user_id'] == event['creator_id']:
                    self.__attendee_dao.leave_event(attendee_id, eventId)
                else:
                    # neither creator or the target user
                    raise ServiceException(
                        'Only the creator can remove other users from an event'
                    )
        except BaseAppException as e:
            # Handle DAO/Validation errors
            raise ServiceException(str(e))
        except Exception as e:
            # Handle unexpected errors
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while leaving this info.'
            )

        return Response(status=200)
