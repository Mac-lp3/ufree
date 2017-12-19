import os
from test.classes.connection import Connection

class psycopg2:

    def __init__ (self):
        print('Mock Psycopg2 Initialized')

    def connect (self, str):
        print('connecting to', str)
        c = Connection(str)
        return c
