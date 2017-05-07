import re
import datetime

class ApiInputValidator:

	#just letters, numbers, and spaces
	event_name_pattern = re.compile('[-!$%^&*()_+|~=`{}\[\]:";\'<>?,.\/]')
	event_name_length = 50
	event_creator_pattern = re.compile('[-!$%^&*()_+|~=`{}\[\]:";\'<>?,.\/]')
	event_creator_length = 25

	def validate_event(eventObject):
		'''
		Validates each field of the event object.

		Returns a list of error messages or an empty list if none found.
		'''

		error_messages = []

		# Validate name field
		if not isinstance(eventObject['name'], str):
			error_messages.append('Name must be a string')

		if len(eventObject['name']) > ApiInputValidator.event_name_length:
			message = 'Name must be less than {0} characters'.format(
				ApiInputValidator.event_name_length
			)
			error_messages.append()

		if re.search(ApiInputValidator.event_name_pattern , eventObject['name']):
			error_messages.append('Name must only contain letters or numbers')

		# Validate creator field
		if not isinstance(eventObject['creator'], str):
			error_messages.append('Creator must be a string')

		if len(eventObject['creator']) > ApiInputValidator.event_creator_length:
			message = 'Creator must be less than {0} characters'.format(
				ApiInputValidator.event_creator_length
			)
			error_messages.append(message)

		if re.search(ApiInputValidator.event_creator_pattern, eventObject['creator']):
			error_messages.append('Creator must only contain letters or numbers')

		return error_messages
