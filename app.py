from flask import Flask, render_template, request, abort, jsonify, Response
from raven.contrib.flask import Sentry
from delorean import DeLorean, NotWellFormedException
from hack_hash import hack_hash
from date_hash import date_hash
import simple_encoding
import os
import random
import statsd

statsd_client = statsd.StatsClient(os.environ.get('STATSD_HOST', ''), 8125)

def incr_stat(name):
    statsd_client.incr('puzzle.codes.%s' % name)


app = Flask(__name__)
sentry = Sentry(app)

if 'SECRET_KEY' in os.environ:
    app.SECRET_KEY = os.environ['SECRET_KEY']

with open('script.txt', 'r') as f:
    app.delorean = DeLorean(f.read())

ANSWER_TEMPLATE = 'the %s of %s but like %s'

COMPANIES_1 = [
    'airware', 'amazon', 'apple', 'atlassian', 'blend', 'box',
    'cisco', 'de shaw', 'docker', 'dropbox', 'ebay', 'evernote',
    'fidelity', 'github', 'groupon',
    'hubspot', 'ibm', 'intuit', 'kayak', 'lastpass', 'logitech',
    'mailchimp', 'microsoft', 'mozilla', 'nvidia', 'oracle', 'pandora',
    'pinterest', 'quizlet', 'redhat', 'slack', 'spacex',
    'stripe', 'thumbtack', 'tumblr', 'twitch', 'uber', 'valve',
    'whatsapp', 'yahoo', 'zappos', 'zillow'
]
INDUSTRIES = [
    'agriculture', 'art', 'beauty', 'clean tech',
    'buildings', 'consulting', 'consumers', 'marketing',
    'ecommerce', 'education', 'energy', 'fashion',
    'fin tech', 'health care', 'health', 'hotels',
    'hr', 'iot', 'bio',
    'logistics', 'groceries', 'media', 'nonprofits', 'real estate',
    'restaurants', 'retail', 'sports', 'travel'
]
COMPANIES_2 = [
    'airbnb', 'akamai', 'asana', 'barclays',
    'bloomberg', 'braintree', 'cruise', 'aws',
    'duolingo', 'etsy', 'facebook', 'fitbit',
    'galois', 'godaddy', 'google', 'houzz', 'hulu', 'intel',
    'jane st', 'linkedin', 'lyft', 'medium',
    'mongodb', 'nest', 'openai', 'palantir', 'paypal', 'qualcomm',
    'quora', 'sendgrid', 'snap', 'square', 'tesla',
    'tinder', 'twilio', 'twitter', 'unity', 'disney', 'xero',
    'yelp', 'zenefits', 'zynga'
]

# validate companies
content_length = max(map(len, COMPANIES_1)) + \
    max(map(len, INDUSTRIES)) + max(map(len, COMPANIES_2))
ans_length = len(ANSWER_TEMPLATE % ('', '', ''))
max_length = content_length + ans_length
print('max length delorean str %i' %
      (app.delorean.max_bits // simple_encoding.BITS))
assert max_length <= app.delorean.max_bits // simple_encoding.BITS


EXAMPLE_STRS = [
    'great scott',
    'eighty eight mph',
    'get your hands off her'
]



@app.route('/')
def index():
    return '/u/&lt;ur_github&gt;'


@app.route('/u/<username>/')
def page(username):
    resp = Response(render_template('index.html'))
    token_strategy = 'lower,newlines->spaces,drop-non-lettersspaces'
    resp.headers['X-Script'] = '/static/script.txt'
    resp.headers['X-Tokenization-Strategy'] = token_strategy
    return resp


def get_answer_str(username):
    company_1 = hack_hash(username + app.SECRET_KEY, COMPANIES_1, 1)
    industry = hack_hash(username + app.SECRET_KEY, INDUSTRIES, 1)
    company_2 = hack_hash(username + app.SECRET_KEY, COMPANIES_2, 1)
    return ANSWER_TEMPLATE % (company_1, industry, company_2)


@app.route('/api/examples')
def examples():
    incr_stat('examples')
    examples = []
    for example in EXAMPLE_STRS:
        example_bits = simple_encoding.encode(example)
        delorean_message = app.delorean.encode_without_permutation(
            example_bits)
        random.shuffle(delorean_message)
        examples.append({
            'message': example,
            'message_bits': example_bits,
            'codeword': ' '.join(delorean_message)
        })
    return jsonify(examples)


@app.route('/api/challenge/')
def challenge():
    if 'username' not in request.args:
        abort(400)
    username = request.args['username']
    answer_str = get_answer_str(username)
    incr_stat('challenge')

    response = {
        'message': answer_str,
        'message_bits': simple_encoding.encode(answer_str)
    }
    return jsonify(response)


@app.route('/api/decode/', methods=['POST'])
def decode():
    if 'codeword' not in request.form or 'username' not in request.form:
        abort(400)
    username = request.form['username']
    word_list = request.form['codeword'].lower().split(' ')

    message_bits = None
    well_formed = False
    answer = None

    incr_stat('decode')

    try:
        message_bits = app.delorean.decode(word_list)
        well_formed = True
        incr_stat('well_formed_decode')
    except NotWellFormedException:
        pass

    # the_message_they_shouldve_sent =
    # app.delorean.encode_without_permutation(get_answer(username))
    answer_str = get_answer_str(username)
    answer_bits = simple_encoding.encode(answer_str)

    if message_bits == answer_bits:
        incr_stat('correct_decode')
        answer = date_hash(app.secret_key, username)

    message_str = None
    try:
        if message_bits is not None:
            message_str = simple_encoding.decode(message_bits)
    except:
        pass

    response = {
        'well_formed': well_formed,
        'message_bits': message_bits,  # bitstring
        'message': message_str,
        'answer': answer
    }

    return jsonify(response)

@app.route('/healthz/')
def status():
    return 'OK'

if __name__ == '__main__':
    app.SECRET_KEY = 'abcdsafkdsajf'
    app.run(debug=True)
