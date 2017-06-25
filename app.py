from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/api/decode', methods=['POST'])
def decoder():
    codeword = request.form['codeword']
    return jsonify({
        'message': len(codeword),
        'well_formed': True,
        'answer': None
    })

if __name__ == '__main__':
    app.run(debug=True)
