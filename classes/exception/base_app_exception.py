import json

class BaseAppException(Exception):

    def __init__(self, messages):
        super()
        self.messages = messages

    def get_payload(self):
        return json.dumps({
            'errors': self.messages
        })
