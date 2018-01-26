import os
import re
import builtins
import importlib
from classes.exception.provider_exception import ProviderException

class DependencyProvider:

    def get_instance (self, class_name):
        target = None
        package = ''
        target_class = None
        try:
            if 'dao' in class_name.lower():
                package = builtins.daos_package
            elif 'filter' in class_name.lower():
                package = builtins.filters_package
            elif 'service' in class_name.lower():
                package = builtins.services_package
            elif 'psycopg2' in class_name.lower():
                package = builtins.psycopg2_package
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