from delorean import DeLorean
import unittest
import random


class DeLoreanTests(unittest.TestCase):
    def test_wfc(self):
        corpus = 'hi my name is pat what is your name'
        words = ['hi', 'my', 'name', 'is', 'pat', 'what', 'is', 'your', 'name']
        self.assertEqual(DeLorean.words_from_corpus(corpus), words)

    def test_uwobfo(self):
        words = ['hi', 'my', 'name', 'is', 'pat', 'what', 'is', 'your', 'name']
        result = DeLorean.unique_words_sorted_by_first_occurence(words)
        expected = ['hi', 'my', 'name', 'is', 'pat', 'what', 'your']
        self.assertEqual(result, expected)

    def test_truncate_extra_words(self):
        words = ['hi', 'my', 'name', 'is', 'pat']
        d = DeLorean('', bucket_size=2, n=1)
        result = d.truncate_extra_words(words)
        expected = ['hi', 'my', 'name', 'is']
        self.assertEqual(result, expected)

    def test_encode_nbs(self):
        corpus = 'hi my name is pat what is your name'
        d = DeLorean(corpus, bucket_size=2, n=1)

        self.assertEqual(d.encode_N_bs('0', 0), 'hi')
        self.assertEqual(d.encode_N_bs('1', 0), 'my')

        self.assertEqual(d.encode_N_bs('0', 1), 'name')
        self.assertEqual(d.encode_N_bs('1', 1), 'is')

    def test_encode_without_permutation(self):
        # TODO test for padding??
        corpus = 'hi my name is pat what is your name'
        d = DeLorean(corpus, bucket_size=2, n=1)

        self.assertEqual(d.encode_without_permutation('00'), ['hi', 'name'])
        self.assertEqual(d.encode_without_permutation('10'), ['my', 'name'])
        self.assertEqual(d.encode_without_permutation('11'), ['my', 'is'])

    def test_decode_sorted(self):
        encoded = ['hi', 'is']

        corpus = 'hi my name is pat what is your name'
        d = DeLorean(corpus, bucket_size=2, n=1)

        self.assertEqual(d.decode_sorted(['hi', 'name']), '00')
        self.assertEqual(d.decode_sorted(['my', 'is']), '11')
        self.assertEqual(d.decode_sorted(['hi', 'is']), '01')

    def test_end_to_end(self):
        with open('script.txt', 'r') as f:
            corpus = f.read()
        d = DeLorean(corpus)
        for i in range(12):
            inp = ''.join(random.choice(['0', '1']) for _ in range(d.max_bits))
            inp = inp[:-i]
            encoded = d.encode_without_permutation(inp)
            random.shuffle(encoded)
            decoded = d.decode(encoded)
            while len(inp) % d.n != 0:
                inp += '0'
            self.assertEqual(decoded, inp)


if __name__ == '__main__':
    unittest.main()
