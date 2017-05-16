class Cursor:
    def __init__(self):
        print('initing')

    def execute (self, string):
        print('mocking ' + string)

    def fetchone (self):
        print('fetching one...')
        return True

    def fetchall (self):
        print('fetching all...')
