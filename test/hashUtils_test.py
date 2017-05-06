import os
import unittest

dir_path = os.path.dirname(os.path.realpath(__file__))
fts = os.path.join(dir_path, '..\classes\HashCodeUtils.py')
exec(open(fts).read())

class HashCodeUtilsTest(unittest.TestCase):

	def test_hash_method(self):
		seedToUse = 'Tom\'s cool hang out thing!'

		print('Using seed: ' + seedToUse)

		genCode = HashCodeUtils.generate_code(seedToUse)

		print(genCode)

if __name__ == '__main__':
	unittest.main()
