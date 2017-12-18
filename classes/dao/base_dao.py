import os
import sys
import importlib

class BaseDao ():

    def __init__ (self):
        if os.environ['ENV'] == 'test':
            temp = importlib.import_module('test.classes.psycopg2')
        else:
            temp = importlib.import_module('psycopg2')
        psycopg2 = temp.psycopg2()

        try:
            db_conn_str = 'dbname=' + os.environ['DB_NAME']
            conn = psycopg2.connect(db_conn_str)
            self._cur = conn.cursor()
        except ImportError:
            print(ImportError)
        except:
            print(sys.exc_info())
            print('I am unable to connect to the database')
