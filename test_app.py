import unittest
import app
import json
import simple_encoding


class AppTest(unittest.TestCase):
    def setUp(self):
        app.app.SECRET_KEY = 'adfdsfsd'
        self.app = app.app.test_client()

    def test_challenge(self):
        rv = self.app.get('/api/challenge?username=patins')
        j = json.loads(rv.data)
        answer_str = app.get_answer_str('patins')
        self.assertEqual(j['message'], answer_str)
        self.assertEqual(j['message_bits'], simple_encoding.encode(answer_str))

    def decode(self, s):
        rv = self.app.post(
            '/api/decode', data={'username': 'patins', 'codeword': s})
        return json.loads(rv.data)

    def test_decode_invalid(self):
        r = self.decode('jfslkdafjsldjfsodijvcsao')
        self.assertEqual(r, {
            'answer': None,
            'message': None,
            'message_bits': None,
            'well_formed': False
        })

    def test_decode_valid_invalid_encoding(self):
        r = self.decode('back')
        self.assertEqual(r, {
            'answer': None,
            'message': 'a',
            'message_bits': '00000',
            'well_formed': True
        })

    def test_decode_valid(self):
        r = self.decode('back on')
        self.assertEqual(r, {
            'answer': None,
            'message': 'aa',
            'message_bits': '0000000000',
            'well_formed': True
        })

    def test_decode_answer(self):
        answer_str = app.get_answer_str('patins')
        answer_bits = simple_encoding.encode(answer_str)
        answer = app.app.delorean.encode_without_permutation(
            answer_bits)
        r = self.decode(' '.join(answer))
        self.assertIsNotNone(r['answer'])
        self.assertTrue(r['well_formed'])
        self.assertEqual(r['message'], answer_str)
        self.assertEqual(r['message_bits'], answer_bits)

    def test_example(self):
        rv = self.app.get('/api/examples')
        examples = json.loads(rv.data)
        for example in examples:
            self.assertEqual(example['message_bits'],
                             simple_encoding.encode(example['message']))
            self.assertEqual(simple_encoding.decode(
                example['message_bits']), example['message'])
            self.assertCountEqual(
                app.app.delorean.encode_without_permutation(
                    example['message_bits']),
                example['codeword'].split(' ')
            )
            self.assertEqual(
                app.app.delorean.decode(example['codeword'].split(' ')),
                example['message_bits']
            )


if __name__ == '__main__':
    unittest.main()
