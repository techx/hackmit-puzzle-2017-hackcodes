from flask import Flask, render_template, request, abort, jsonify
from delorean import DeLorean, NotWellFormedException
from hack_hash import hack_hash

app = Flask(__name__)
with open('script.txt', 'r') as f:
  app.delorean = DeLorean(f.read())

@app.route('/')
def index():
  return '/u/&lt;ur_github&gt;'

def get_answer(username):
  return hack_hash(username + app.SECRET_KEY, ['0', '1'], app.delorean.max_bits)

@app.route('/api/challenge')
def challenge():
  if 'username' not in request.args:
    abort(400)
  username = request.args['username']
  response = {
    'message': get_answer(username)
  }
  return jsonify(response)

@app.route('/api/decode', methods=['POST'])
def decode():
  if 'codeword' not in request.form or 'username' not in request.form:
    abort(400)
  username = request.form['username']
  word_list = request.form['codeword'].split(' ')

  message = None
  well_formed = False
  answer = None

  try:
    message = app.delorean.decode(word_list)
    well_formed = True
  except NotWellFormedException:
    pass

  #the_message_they_shouldve_sent = app.delorean.encode_without_permutation(get_answer(username))

  if message == get_answer(username):
    answer = 'YOU DID IT'

  response = {
    'well_formed': well_formed,
    'message': message, #bitstring
    'answer': answer
  }

  return jsonify(response)

if __name__ == '__main__':
  app.SECRET_KEY = 'abcdsafkdsajf'
  app.run(debug=True)
