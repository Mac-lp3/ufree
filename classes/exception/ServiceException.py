import json
from classes.exception.BaseAppException import BaseAppException

class ServiceException(BaseAppException):
	def get_payload (self):
		return json.dumps({
			'errors': self.message
		})
