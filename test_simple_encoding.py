import unittest
import simple_encoding


class TestSimpleEncoding(unittest.TestCase):
    def test_char_to_bits(self):
        b = simple_encoding.encode('a')
        self.assertEqual(b, '00000000')

        b = simple_encoding.encode('b')
        self.assertEqual(b, '00000001')

    def test_end_to_end(self):
        inp = 'hi my name is pat what is your name'

        encoded = simple_encoding.encode(inp)
        decoded = simple_encoding.decode(encoded)

        self.assertEqual(decoded, inp)
