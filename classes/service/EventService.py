import os
import sys
import json
import inspect
import importlib
from classes.provider.DependencyProvider import DependencyProvider
from classes.util.HashCodeUtils import HashCodeUtils
from classes.util.EventValidator import EventValidator
from classes.util.AttendeeValidator import AttendeeValidator
from classes.exception.ServiceException import ServiceException
from classes.exception.BaseAppException import BaseAppException

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
        response_body = {}
        try:
            # validate
            eventId = req.matchdict['eventId']
            self.__eventValidator.validate_event_id(eventId)
            data = self.__event_dao.load_event(eventId)
            json_data = json.dumps(data)
            response_body = json_data
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while loading this event.'
            )
        return response_body

    def update_event (self, req):
        response_body = {}
        try:
            payload = req.json_body
            self.__eventValidator.validate_event(payload)
            data = self.__event_dao.update_event(payload)
            json_data = json.dumps(data)
            response_body = json_data
        except BaseAppException as e:
            raise ServiceException(str(e))
        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while updating this event.'
            )
        return response_body

    def create_event (self, req):
        '''
        Creates a new event.

        Validates the request object, extracts all required information, and
        builds the event and associated objects.
        '''
        # TODO year mechanism.
        response_body = {}
        try:
            inputErrors = self.__eventValidator.validate_event(req.json_body)

            if not inputErrors:
                # set the creator_id and save the event
                req.json_body['creator_id'] = req.cookies['user_id']
                data = self.__event_dao.save_event(req.json_body)

                # build the response body
                json_data = json.dumps(data)
                response_body = json_data

            else:
                response_body = json.dumps(inputErrors)
        except BaseAppException as e:
            raise ServiceException(str(e))

        except Exception as e:
            print(e, sys.exc_info())
            raise ServiceException('An error occurred while creating this event.')

        return response_body

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

    def add_event_attendee (self, req):
        '''
        Adds the user to the event.

        Only the user making the request can join an event. Users cannot be
        added to an event by another user.
        '''

        try:
            # validate the attendee object
            self.__attendeeValidator.validate_attendee_request(req)

            # validate the event id
            eventId = req.matchdict['eventId']
            self.__eventValidator.validate_event_id(eventId)

            # get the user id from the request and add it to attendee list
            req.json_body['id'] = req.cookies['user_id']
            self.__attendee_dao.join_event(req.json_body, eventId)

        except BaseAppException as e:
            # Handle DAO/Validation errors
            raise ServiceException(str(e))
        except Exception as e:
            # Handle unexpected errors
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while joining this event.'
            )

    def update_event_attendee (self, req):
        response_body = {}
        try:
            if 'id' not in req.json_body:
                raise ServiceException('Id was not found on this request')
            inputErrors = self.__attendeeValidator.validate_attendee_request(req)
            data = self.__attendee_dao.update_attendee(req.json_body)
            json_data = json.dumps(data)
            response_body = json_data
        except BaseAppException as e:
            # Handle DAO/Validation errors
            raise ServiceException(str(e))
        except Exception as e:
            # Handle unexpected errors
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while updating your info.'
            )
        return response_body

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

    def get_event_attendees (self, req):
        try:
            # validate the event id
            eventId = req.matchdict['eventId']
            self.__eventValidator.validate_event_id(eventId)

            # load the attendee list
            data = self.__attendee_dao.load_attendees(eventId)

            # build response object
            json_data = json.dumps(data)
            response_body = json_data

        except BaseAppException as e:
            # Handle DAO/Validation errors
            raise ServiceException(str(e))
        except Exception as e:
            # Handle unexpected errors
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while retrieving attendee list.'
            )
        return response_body

    def update_attendee_availability (self, req):
        req_body = req.json_body
        response_body = {}
        try:
            # TODO validate availability
            #inputErrors = self.__eventValidator.validate_attendee(req_body)
            data = self.__availability_dao.update_availability(req_body)
            json_data = json.dumps(data)
            response_body = json_data
        except BaseAppException as e:
            # Handle DAO/Validation errors
            raise ServiceException(str(e))
        except Exception as e:
            # Handle unexpected errors
            print(e, sys.exc_info())
            raise ServiceException(
                'An error occurred while updating availability.'
            )
        return response_body
