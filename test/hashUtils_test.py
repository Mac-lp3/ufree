import unittest
from classes.HashCodeUtils import HashCodeUtils

class HashCodeUtilsTest(unittest.TestCase):

	def test_hash_method(self): 
		seedToUse = 'Tom\'s cool hang out thing!'

		print('Using seed: ' + seedToUse)

		genCode = HashCodeUtils.generate_code(seedToUse)

		print(genCode)

if __name__ == '__main__':
	unittest.main()