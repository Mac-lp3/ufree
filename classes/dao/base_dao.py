import os
import sys
import importlib
from classes.provider.dependency_provider import DependencyProvider

class BaseDao ():

    def __init__ (self):
        self.__provider = DependencyProvider()
        self.__psycopg2 = self.__provider.get_instance('psycopg2')

        try:
            db_conn_str = 'dbname=' + os.environ['DB_NAME']
            conn = self.__psycopg2.connect(db_conn_str)
            self._cur = conn.cursor()
        except ImportError:
            print(ImportError)
        except:
            print(sys.exc_info())
            print('I am unable to connect to the database')
