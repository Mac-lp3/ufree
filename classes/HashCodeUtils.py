class HashCodeUtils:

	def generate_code(seed):
		'''
		Generates a new 64 bit FNV-1a hash with the provided seed.
		'''

		hval = 0x811c9dc5
		fnv_32_prime = 0x01000193
		uint32_max = 2 ** 32
		for s in seed:
			hval = hval ^ ord(s)
			hval = (hval * fnv_32_prime) % uint32_max

		return hval
