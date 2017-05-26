class BaseAppException(Exception):

	def __init__ (self, message):
		super()
		self.message = message

	def get_payload (self):
		return self.message
