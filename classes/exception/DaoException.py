from classes.exception.BaseAppException import BaseAppException

class DaoException(BaseAppException):
	def get_payload (self):
		return json.dumps({
			'errors': self.message
		})
