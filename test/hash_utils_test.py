import os
import unittest
import hashlib
from classes.util.hash_utils import HashUtils

# dir_path = os.path.dirname(os.path.realpath(__file__))
# fts = os.path.join(dir_path, '..\classes\util\HashUtils.py')
# exec(open(fts).read())

class HashUtilsTest(unittest.TestCase):

    def setUp(self):
        self.__seedToUse = 'Tom\'s cool hang out thing!'
        self.__starHashCharacter = '1dvr2tg5l39dpvja8d8sb1h2dnw*askb'
        self.__dotHashCharacter = '1dvr2tg5l39dpvja8d8sb1h2dnw.askb'
        self.__openHashCharacter = '1dvr2tg5l39dpvja8d8sb1h2dnw(askb'
        self.__shortHashLength = '1dvr2tg5l39dpvja8d8sb1h2dnwaskb'
        self.__longHashLength = '1dvr2tg5l39dpvja8d8sb1h2dnwaskb3t'
        self.__goodHash = ''

    def test_hash_method (self):
        print('Using seed: ' + self.__seedToUse)
        genCode = HashUtils.generate_code(self.__seedToUse)
        print(genCode)
        self.assertEqual(len(genCode), 32)
        self.__goodHash = genCode

    def test_hash_validation (self):
        test_messages = HashUtils.validate_hash(self.__starHashCharacter)
        self.assertEqual(len(test_messages), 1)

        test_messages = HashUtils.validate_hash(self.__dotHashCharacter)
        self.assertEqual(len(test_messages), 1)

        test_messages = HashUtils.validate_hash(self.__openHashCharacter)
        self.assertEqual(len(test_messages), 1)

        test_messages = HashUtils.validate_hash(self.__shortHashLength)
        self.assertEqual(len(test_messages), 1)

        test_messages = HashUtils.validate_hash(self.__longHashLength)
        self.assertEqual(len(test_messages), 1)

        self.__goodHash = HashUtils.generate_code(self.__seedToUse)
        test_messages = HashUtils.validate_hash(self.__goodHash)
        self.assertEqual(len(test_messages), 0)

if __name__ == '__main__':
    unittest.main()
