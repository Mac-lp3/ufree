import os
import re
import importlib
from classes.exception.provider_exception import ProviderException

class DependencyProvider:

    __is_prod = False
    __daos_prefix = 'test.classes.'
    __filters_prefix = 'test.classes.'
    __psycopg2_prefix = 'test.classes.'
    __services_prefix = 'test.classes.'

    def __init__ (self):
        if os.environ['ENV'] == 'production':
            self.__is_prod = True
            self.__daos_prefix = 'classes.dao.'
            self.__filters_prefix = 'classes.filter.'
            self.__services_prefix = 'classes.service.'
            self.__psycopg2_prefix = ''

    def get_instance (self, class_name):
        target = None
        package = ''
        target_class = None
        try:
            if 'dao' in class_name.lower():
                package = self.__daos_prefix
            if 'filter' in class_name.lower():
                package = self.__filters_prefix
            if 'service' in class_name.lower():
                package = self.__services_prefix
            if 'psycopg2' in class_name.lower():
                package = self.__psycopg2_prefix
            target_class = importlib.import_module(
                package + self.to_snake_case(class_name)
            )
            target = getattr(target_class, class_name)
        except Exception as e:
            raise ProviderException(
                'Could not locate dependency ' + class_name + ' in ' + package
            )

        target = getattr(target_class, class_name)
        target = target()
        
        return target

    def to_snake_case(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()