class MockRequest():

    matchdict = {}
    json_body = {}
    cookies = {}

    def __init__ (self, id={}, body={}, cookies={}):
        if id:
            self.matchdict = {'eventId': id}
        if body:
            self.json_body = body
        if cookies:
            self.cookies = cookies
