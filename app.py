from flask import Flask, render_template, request, abort, jsonify, Response
from raven.contrib.flask import Sentry
from delorean import DeLorean, NotWellFormedException
from hack_hash import hack_hash
import simple_encoding
import os
import sys

app = Flask(__name__)
sentry = Sentry(app)

if 'SECRET_KEY' in os.environ:
    app.SECRET_KEY = os.environ['SECRET_KEY']

with open('script.txt', 'r') as f:
    app.delorean = DeLorean(f.read())

with open('projects.txt', 'r') as f:
    projects_unfiltered = f.read().strip().split('\n')
    PROJECTS = []
    length = app.delorean.max_bits // simple_encoding.BITS
    for project in projects_unfiltered:
        if len(project) >= length:
            PROJECTS.append(project[:length].strip())
    if len(PROJECTS) == 0:
        print("NOT ENOUGH PROJECTS")
        sys.exit(1)
    print("loaded %i projects" % len(PROJECTS))


@app.route('/')
def index():
    return '/u/&lt;ur_github&gt;'


@app.route('/u/<username>')
def page(username):
    resp = Response(render_template('index.html'))
    token_strategy = 'lower,newlines->spaces,drop-non-lettersspaces'
    resp.headers['X-Script'] = '/static/script.txt'
    resp.headers['X-Tokenization-Strategy'] = token_strategy
    return resp


def get_answer_str(username):
    # 5 is the max length of one of these strings
    return hack_hash(
        username + app.SECRET_KEY,
        PROJECTS,
        1
    )


@app.route('/api/challenge')
def challenge():
    if 'username' not in request.args:
        abort(400)
    username = request.args['username']
    answer_str = get_answer_str(username)
    response = {
        'message': answer_str,
        'message_bits': simple_encoding.encode(answer_str)
    }
    return jsonify(response)


@app.route('/api/decode', methods=['POST'])
def decode():
    if 'codeword' not in request.form or 'username' not in request.form:
        abort(400)
    username = request.form['username']
    word_list = request.form['codeword'].split(' ')

    message_bits = None
    well_formed = False
    answer = None

    try:
        message_bits = app.delorean.decode(word_list)
        well_formed = True
    except NotWellFormedException:
        pass

    # the_message_they_shouldve_sent =
    # app.delorean.encode_without_permutation(get_answer(username))
    answer_str = get_answer_str(username)
    answer_bits = simple_encoding.encode(answer_str)

    if message_bits == answer_bits:
        answer = 'YOU DID IT'

    try:
        message_str = simple_encoding.decode(message_bits)
    except:
        message_str = None

    response = {
        'well_formed': well_formed,
        'message_bits': message_bits,  # bitstring
        'message': message_str,
        'answer': answer
    }

    return jsonify(response)


if __name__ == '__main__':
    app.SECRET_KEY = 'abcdsafkdsajf'
    app.run(debug=True)
