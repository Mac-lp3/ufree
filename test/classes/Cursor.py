import builtins

class Cursor:
    def __init__(self):
        print('Initializing Cursor')

    def execute (self, string):
        if builtins.db_fail == 'True':
            print('Mocking an exception...')
            raise Exception('some exception')
        print('mocking ' + string)

    def fetchone (self):
        print('fetching one...')
        if builtins.db_fail == 'True':
            print('Mocking an exception...')
            raise Exception('some exception')
        ret = {}
        try:
            if len(builtins.return_pattern) > 0:
                ret = builtins.return_pattern.pop(0)
        except:
            ret = {
                'id': '123123123123',
                'name': 'Kenny K\'s thing',
                'creator': 'Kenny K'
            }
        print('returning', ret)
        return ret

    def fetchall (self):
        if builtins.db_fail == 'True':
            print('Mocking an exception...')
            raise Exception('some exception')
        print('fetching all...')
        col = []
        col.append('123123123123')
        col.append('Kenny K\'s thing')
        col.append('kennyId')
        col.append('20200101')
        row = []
        row.append(col)
        return row
