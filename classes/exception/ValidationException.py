from classes.exception.BaseAppException import BaseAppException

class ValidationException(BaseAppException):
	def get_payload (self):
		return json.dumps({
			'errors': self.messages
		})
