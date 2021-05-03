from flask import Flask, jsonify, request
import pandas as pd

import emoji
import re

from underthesea import word_tokenize

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
    logging.debug("do day roi ne")
    df = pd.read_excel('./data/train_dataset.xlsx', usecols=["id", "comment", "updated_sentiment_2"])

    for i in range(0, 10):
        print("sentence", i)
        sentence = df["comment"][i]
        print(sentence)
        demojize = emoji.demojize(sentence)
        clean = remove_special_text(demojize)
        print("clean", clean)
        w_tokens = word_tokenize(clean)
        if "," in w_tokens:
            w_tokens.remove(",")
        print("w_tokens", w_tokens)


        # demojize = []
        # for w in range(len(w_tokens)):
        #     demojize.append(emoji.demojize(w_tokens[w]))
        # demojize = emoji.demojize(w_tokens)
        # print("demojize", demojize)


def remove_special_text(text):
    return re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", ' ', text)


# def tokenize_sentences(sentences):
#     """ọec
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
