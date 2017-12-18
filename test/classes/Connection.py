from test.classes.cursor import Cursor

class Connection:

    __string = ''

    def __init__ (self, str):
        self.__string = str

    def cursor (self):
        c = Cursor()
        return c
