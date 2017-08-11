import os
from classes.exception.ProviderException import ProviderException

class DependencyProvider:

    is_prod = False
    daos_prefix = 'test.classes.'
    filters_prefix = 'test.classes.'

    def __init__ (self):
        if os.environ['ENV'] == 'production':
            self.is_prod = True
            daos_prefix = 'classes.dao.'
            filters_prefix = 'classes.filter.'

    def get_instance (self, class_name):
        target = none
        if 'dao' in class_name.lower()
            try:
                target = importlib.import_module(daos_prefix + class_name)
            except Exception as e:
                message = 'Could not locate dependency' +
                    class_name + 'in' + daos_prefix
                raise ProviderException(message)
        if 'filter' in class_name.lower()
            try:
                target = importlib.import_module(filters_prefix + class_name)
            except Exception as e:
                message = 'Could not locate dependency' +
                    class_name + 'in' + filters_prefix
                raise ProviderException(message)
        return target
