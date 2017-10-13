class MockRequest():

    matchdict = {
        'eventId': None,
        'attendee_id': None,
        'availability_id': None
    }
    json_body = {}
    cookies = {}
    method = 'GET'

    def __init__ (
        self,
        event_id={},
        body={},
        cookies={},
        attendee_id={},
        availability_id={},
        method='GET'
    ):
        if event_id:
            self.matchdict['eventId'] = event_id
        if attendee_id:
            self.matchdict['attendee_id'] = attendee_id
        if availability_id:
            self.matchdict['availability_id'] = availability_id
        if body:
            self.json_body = body
        if cookies:
            self.cookies = cookies
        self.method = method
