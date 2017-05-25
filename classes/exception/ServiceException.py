import json

class ServiceException(Exception):
	def get_payload (self):
		return json.dumps({
			'error': self.message
		})
