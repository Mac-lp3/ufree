import json

class BaseAppException(Exception):

	def __init__ (self, payload):
		super()
		self.payload = payload

	def get_payload (self):
		return json.dumps({
			'errors': self.payload
		})
