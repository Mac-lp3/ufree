import os
import re
import importlib
from classes.exception.provider_exception import ProviderException

class DependencyProvider:

    def get_instance(self, class_name):
        target = None
        package = ''
        target_class = None
        try:
            if 'dao' in class_name.lower():
                package = os.environ['DAOS_PACKAGE']
            elif 'filter' in class_name.lower():
                package = os.environ['FILTERS_PACKAGE']
            elif 'service' in class_name.lower():
                package = os.environ['SERVICES_PACKAGE']
            elif 'psycopg2' in class_name.lower():
                package = os.environ['PSYCOPG2_PACKAGE']
            target_class = importlib.import_module(
                package + self.to_snake_case(class_name)
            )
            target = getattr(target_class, class_name)
        except Exception as exception:
            print('exception in dependency provider:', exception)
            print('env vars:', os.environ)
            raise ProviderException(
                'Could not locate dependency ' + class_name + ' in ' + package
            )

        target = getattr(target_class, class_name)
        target = target()
        return target

    def to_snake_case(self, name):
        sub_str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', sub_str).lower()
