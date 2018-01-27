import os
import builtins

class Cursor:
    def __init__(self):
        print('Initializing Cursor')

    def execute (self, string):
        if os.environ['TEST_DB_FAIL'] == 'True':
            print('Mocking an exception...')
            raise Exception('some exception')
        print('mocking ' + string)

    def fetchone (self):
        print('fetching one...')
        if os.environ['TEST_DB_FAIL'] == 'True':
            print('Mocking an exception...')
            raise Exception('some exception')
        if isinstance(builtins.db_return_object, list):
            ret = builtins.db_return_object.pop()
        else:
            ret = builtins.db_return_object
        print('returning', ret)
        return ret

    def fetchall (self):
        if os.environ['TEST_DB_FAIL'] == 'True':
            print('Mocking an exception...')
            raise Exception('some exception')
        print('fetching all...')
        return builtins.db_return_object
