from flask import Flask, jsonify, request
import pandas as pd


import logging
logging.basicConfig(
    filename='runtime.log',
    filemode='w',
    level=logging.DEBUG,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return {
        'hello': 'world'
    }


@app.route('/nlp-test', methods=['GET'])
def homework_nlp():
    return {
        'hello': 'world'
    }


if __name__ == '__main__':
    # homework_nlp()
    app.run(debug=True, host='0.0.0.0', port=5000)
