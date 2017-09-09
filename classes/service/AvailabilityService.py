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

        # delete all availability obs for this event

        # get all availability obs for this attendee

        # get availability ob for this attendee

        # add availability ob for this attendee

        # update availability ob for this attendee

        # delte availability ob for this attendee

        # delete all availability obs for this attendee
