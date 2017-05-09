import os
import unittest

dir_path = os.path.dirname(os.path.realpath(__file__))
fts = os.path.join(dir_path, '..\\views\\api.py')
exec(open(fts).read())

class ApiTest(unittest.TestCase):

    def get_event_test (self):
        print(get_event)
        resp = get_event({'eventId': '123123123123123'})
        print('The resp', resp)

if __name__ == '__main__':
	unittest.main()
