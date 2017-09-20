class MockRequest():

    matchdict = {}
    json_body = {}
    cookies = {}
    method = 'GET'

    def __init__ (self, event_id={}, body={}, cookies={}, attendee_id={}, method='GET'):
        if id:
            self.matchdict['eventId'] = event_id
        if attendee_id:
            self.matchdict['attendee_id'] = attendee_id
        if body:
            self.json_body = body
        if cookies:
            self.cookies = cookies
        self.method = method
