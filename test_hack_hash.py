import unittest
from hack_hash import hack_hash
import string

class HackHashTest(unittest.TestCase):
    def test_singlechar_element(self):
        r = hack_hash('abc', ['a', 'b'], 2)
        self.assertIn(r, ['ab', 'ba', 'aa', 'bb'])
    def test_multichar_element(self):
        r = hack_hash('abc', ['ab', 'bc'], 2)
        self.assertIn(r, ['abab', 'bcab', 'abbc', 'bcbc'])

if __name__ == "__main__":
    unittest.main()
