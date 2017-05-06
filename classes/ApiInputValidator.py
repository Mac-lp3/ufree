import re
import datetime
import HashCodeUtils

class ApiInputValidator:

	#just letters, numbers, and spaces
	namePattern = re.compile('[a-zA-Z\d\s]')

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
