class MockRequest():

    matchdict = {}
    json_body = {}
    cookies = {}

    def __init__ (self, id={}, body={}, cookies={}, attendee_id={}):
        if id:
            self.matchdict['eventId'] = id
        if attendee_id:
            self.matchdict['attendee_id'] = attendee_id
        if body:
            self.json_body = body
        if cookies:
            self.cookies = cookies
