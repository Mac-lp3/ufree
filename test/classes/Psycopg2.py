import os
import classes.exception.DaoException as DaoException
from classes.HashCodeUtils import HashCodeUtils

class psycopg2:
    def connect (str):
        return new Connection()

class Connection:
    def cursor ():
        return new Cursor()

class Cursor:
    def execute (string):
        print('mocking ' + string)

    def fetchone ():
        print('fetching one...')

    def fetchall ():
        print('fetching all...')
