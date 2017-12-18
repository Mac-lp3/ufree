import os
import unittest
import hashlib
from classes.util.hash_utils import HashCodeUtils

# dir_path = os.path.dirname(os.path.realpath(__file__))
# fts = os.path.join(dir_path, '..\classes\util\HashCodeUtils.py')
# exec(open(fts).read())

class HashCodeUtilsTest(unittest.TestCase):

    seedToUse = 'Tom\'s cool hang out thing!'
    starHashCharacter = '1dvr2tg5l39dpvja8d8sb1h2dnw*askb'
    dotHashCharacter = '1dvr2tg5l39dpvja8d8sb1h2dnw.askb'
    openHashCharacter = '1dvr2tg5l39dpvja8d8sb1h2dnw(askb'
    shortHashLength = '1dvr2tg5l39dpvja8d8sb1h2dnwaskb'
    longHashLength = '1dvr2tg5l39dpvja8d8sb1h2dnwaskb3t'
    goodHash = ''

    def test_hash_method (self):
        print('Using seed: ' + self.seedToUse)
        genCode = HashCodeUtils.generate_code(self.seedToUse)
        print(genCode)
        self.assertEqual(len(genCode), 32)
        self.goodHash = genCode

    def test_hash_validation (self):
        test_messages = HashCodeUtils.validate_hash(self.starHashCharacter)
        self.assertEqual(len(test_messages), 1)

        test_messages = HashCodeUtils.validate_hash(self.dotHashCharacter)
        self.assertEqual(len(test_messages), 1)

        test_messages = HashCodeUtils.validate_hash(self.openHashCharacter)
        self.assertEqual(len(test_messages), 1)

        test_messages = HashCodeUtils.validate_hash(self.shortHashLength)
        self.assertEqual(len(test_messages), 1)

        test_messages = HashCodeUtils.validate_hash(self.longHashLength)
        self.assertEqual(len(test_messages), 1)

        self.goodHash = HashCodeUtils.generate_code(self.seedToUse)
        test_messages = HashCodeUtils.validate_hash(self.goodHash)
        self.assertEqual(len(test_messages), 0)

if __name__ == '__main__':
    unittest.main()
