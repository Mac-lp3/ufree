import re
import datetime

class ApiInputValidator:

	namePattern = re.compile('[a-zA-Z\d\s]')

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

		elif ApiInputValidator.namePattern.match(eventObject['name']):
			errorMessage.append('Name must only contain letters or numbers')

		return errorMessages

	def validateDateRange(dateRangeObject):
		"""
		Validates a given date range object

		Returns a list of error messages if any problems are found. Returns
		an empty list if none are discovered.
		"""
		errorMessages = []

		if not isinstance(eventObject['from'], str) or not isinstance(eventObject['to'], str):
			errorMessages.append('To/From must be strings')

		else:
			try:
				fromOb = datetime.datetime.strptime(dateRangeObject['from'], '%Y-%m-%d')
				toOb = datetime.datetime.strptime(dateRangeObject['to'], '%Y-%m-%d')

				if fromOb > toOb:
					errorMessages.append('To date must be after From')

			except ValueError:
				errorMessage.append('Date must be in should be YYYY-MM-DD format')

		return errorMessages
