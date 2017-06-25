import unittest
import app
import json


class AppTest(unittest.TestCase):
    def setUp(self):
        app.app.SECRET_KEY = 'adfdsfsd'
        self.app = app.app.test_client()

    def test_challenge(self):
        rv = self.app.get('/api/challenge?username=patins')
        j = json.loads(rv.data)
        self.assertEqual(j['message'], app.get_answer('patins'))

    def decode(self, s):
        rv = self.app.post(
            '/api/decode', data={'username': 'patins', 'codeword': s})
        return json.loads(rv.data)

    def test_decode_invalid(self):
        r = self.decode('jfslkdafjsldjfsodijvcsao')
        self.assertEqual(r, {
            'answer': None,
            'message': None,
            'well_formed': False
        })

    def test_decode_valid(self):
        r = self.decode('back')
        self.assertEqual(r, {
            'answer': None,
            'message': '0000',
            'well_formed': True
        })

    def test_decode_answer(self):
        answer = app.app.delorean.encode_without_permutation(
            app.get_answer('patins'))
        r = self.decode(' '.join(answer))
        self.assertIsNotNone(r['answer'])
        self.assertTrue(r['well_formed'])


if __name__ == '__main__':
    unittest.main()
