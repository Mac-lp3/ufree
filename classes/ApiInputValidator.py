import re
import datetime
import HashCodeUtils

class ApiInputValidator:

	#just letters, numbers, and spaces
	namePattern = re.compile('[a-zA-Z\d\s]')

	#just letters and numbers
	hashPattern = re.compile('[a-zA-Z\d]+$')

	def validate_event_hash(eventHash):
		'''
		Checks the provided string is an acceptable MD5 hash.

		Returns a list of error messages or an empty list if none found.
		'''

		return HashCodeUtils.validate_hash(eventHash)

	def validate_event(eventObject):
		'''
		Validates each field of the event object.

		Returns a list of error messages or an empty list if none found.
		'''

		errorMessages = []

		if not isinstance(eventObject['name'], str):
			errorMessages.append('Name must be a string')

		if len(eventObject['name']) > 30:
			errorMessages.append('Name must be less than 30 characters')

		if not ApiInputValidator.namePattern.match(eventObject['name']):
			errorMessages.append('Name must only contain letters or numbers')

		return errorMessages

	def validate_date_range(dateRangeObject):
		'''
		Validates a given date range object

		Returns a list of error messages if any problems are found. Returns
		an empty list if none are discovered.
		'''

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
