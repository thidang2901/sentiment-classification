from flask import Flask, jsonify, request
import pandas as pd
from pyvi import ViTokenizer
import emoji
import re

import logging as logger
logger.basicConfig(
    filename='runtime.log',
    filemode='w',
    level=logger.DEBUG,
    format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return {
        'hello': 'world'
    }


@app.route('/nlp-test', methods=['GET'])
def homework_nlp():
    logger.debug("do day roi ne")
    df = pd.read_excel('./data/train_dataset.xlsx', usecols=["id", "comment", "updated_sentiment_2"])
    sentence = df["comment"][13]
    print(sentence)
    clean = remove_special_text(sentence)
    print(clean)
    tokens = ViTokenizer.tokenize(clean)
    print(tokens)
    demojize = emoji.demojize(tokens)
    print(demojize)


def remove_special_text(text):
    return re.sub(r'(http\S+)|(@\S+)|RT|\#|!|:|\.|,', ' ', text)

# def tokenize_sentences(sentences):
#     """
#     Tokenize or word segment sentences
#     :param sentences: input sentences
#     :return: tokenized sentence
#     """
#     tokens_list = []
#     for sent in sentences:
#         tokens = tokenizer.tokenize(sent)
#         tokens_list.append(tokens)
#     return tokens_list

if __name__ == '__main__':
    homework_nlp()
    # app.run(debug=True, host='0.0.0.0', port=5000)
