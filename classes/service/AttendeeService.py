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
        pass

    def create_attendee (self, request):
        pass

    def remove_attendee_from_event (self, request):
        pass

    def add_attendee_to_event (self, request):
        pass
