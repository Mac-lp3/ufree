import os
import classes.exception.DaoException as DaoException
from test.classes.Connection import Connection
from classes.HashCodeUtils import HashCodeUtils

class psycopg2:

    def __init__ (self):
        print('Mock Psycopg2 Initialized')

    def connect (self, str):
        print('connecting to', str)
        c = Connection(str)
        return c
