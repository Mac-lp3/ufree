import re
import datetime

class ApiInputValidator:

	#just letters, numbers, and spaces
	namePattern = re.compile('[a-zA-Z\d\s]')

	#just letters and numbers
	hashPattern = re.compile('[a-zA-Z\d]+$')

	def validate_event_hash(eventHash):
		"""
		Checks the provided string to alidates it is a FNV-1a hash.

		A proper FNV-1a hashcode only includes alpha numeric characters
		without spaces.
		"""

		errorMessages = []

		if not isinstance(eventHash, str):
			errorMessages.append('Event hash must be a string')
			
		elif not ApiInputValidator.hashPattern.match(eventHash):
			errorMessages.append('Hash can only include numbers and letters')

		return errorMessages

	def validate_event(eventObject):
		"""
		Validates a given event object.

		Returns a list of error messages if any problems are found. Returns
		an empty list if none are discovered.
		"""

		errorMessages = []

		if not isinstance(eventObject['name'], str):
			errorMessages.append('Name must be a string')

		elif len(eventObject['name']) > 30:
			errorMessages.append('Name must be less than 30 characters')

		elif not ApiInputValidator.namePattern.match(eventObject['name']):
			errorMessages.append('Name must only contain letters or numbers')

		elif hasattr(eventObject, 'dateRanges'):
			for dateRange in eventObject['dateRanges']:
				errorMessages.append(validateDateRange(dateRange))

		return errorMessages

	def validate_date_range(dateRangeObject):
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
