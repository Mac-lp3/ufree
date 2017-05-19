import re
import hashlib

class HashCodeUtils:

	hashPattern = re.compile('[a-zA-Z\d]+$')

	def generate_code (seed):
		'''
		Generates a new 64 bit MD5 hash code with the provided seed.
		'''
		m = hashlib.md5()
		m.update(seed.encode('utf-8'))
		val = m.hexdigest()

		return val

	def validate_hash (hashcode):
		'''
		Validates the given hash is in expected format
		'''
		errorMessages = []

		if not isinstance(hashcode, str):
			errorMessages.append('Event hash must be a string')

		if not HashCodeUtils.hashPattern.match(hashcode):
			errorMessages.append('Hash can only include numbers and letters')

		if len(hashcode) < 32:
			errorMessages.append('Hash is less than 32 characters')

		if len(hashcode) > 32:
			errorMessages.append('Hash is greater than 32 characters')

		return errorMessages
