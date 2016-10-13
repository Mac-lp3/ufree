import re

class ApiInputValidator:

	pattern = re.compile('[a-zA-Z\d\s]')

	def validateEvent(eventObject):
		"""
		Validates a given event object.

		Returns a list of error messages if any problems are found. Returns
		an empty list if none are discovered.
		"""

		errorMessages[0] = ''
		
		if not isinstance(eventObject['name'], str):
			errorMessages[0] = 'Name must be a string'

		elif len(eventObject['name']) > 30:
			errorMessages.append('Name must be less than 30 characters')

		elif ApiInputValidator.pattern.match(eventObject['name']):
			errorMessage.append('Name must only contain letters or numbers')

		return errorMessages

	def validateDateRange(dateRangeObject):
		"""
		Validates a given date range object

		Returns a list of error messages if any problems are found. Returns
		an empty list if none are discovered.
		"""

		print('got to validateDateRange')