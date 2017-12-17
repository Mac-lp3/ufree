import os
import importlib
from classes.exception.provider_exception import ProviderException

class DependencyProvider:

    is_prod = False
    daos_prefix = 'test.classes.'
    filters_prefix = 'test.classes.'
    psycopg2_prefix = 'test.classes.'

    def __init__ (self):
        if os.environ['ENV'] == 'production':
            self.is_prod = True
            daos_prefix = 'classes.dao.'
            filters_prefix = 'classes.filter.'
            services_prefix = 'classes.service.'
            psycopg2_prefix = ''

    def get_instance (self, class_name):
        target = None
        package = ''
        target_class = None
        try:
            if 'dao' in class_name.lower():
                package = self.daos_prefix
            if 'filter' in class_name.lower():
                package = self.filters_prefix
            if 'service' in class_name.lower():
                package = self.services_prefix
            if 'psycopg2' in class_name.lower():
                package = self.psycopg2_prefix
            target_class = importlib.import_module(
                package + class_name
            )
            target = getattr(target_class, class_name)
        except Exception as e:
            raise ProviderException(
                'Could not locate dependency ' + class_name + ' in ' + package
            )

        target = getattr(target_class, class_name)
        target = target()
        
        return target
