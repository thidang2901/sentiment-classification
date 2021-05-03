# -*- coding: utf-8 -*-
"""test-nlp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rmb06VsI605p6usAhRCGUUHAIOZBohyl

# Prepare things

## Install requirements
"""

!pip install underthesea
!pip install emoji

"""## Mount to google drive"""

from google.colab import drive
drive.mount('/content/gdrive')

!ls '/content/gdrive/My Drive/Colab Notebooks/dataset/'

"""# IMPORTANT! Read file into dataframe

*   Check the Google Drive path which contains the dataset file.
*   Input the correct file name, also the column names which are used for comment and sentiment.


"""

path = "/content/gdrive/My Drive/Colab Notebooks"

FILE_NAME = "train_dataset.xlsx"
COMMENT_COLUMN_NAME = "comment"
SENTIMENT_COLUMN_NAME = "sentiment"

import pandas as pd

df = pd.read_excel(f'{path}/dataset/{FILE_NAME}', usecols=["id", COMMENT_COLUMN_NAME, SENTIMENT_COLUMN_NAME])
df.head()

"""# Implement help functions

## Normalized function for some specific cases in vietnamese
"""

import re

slang_dict = {"bình thường": ["bth","bt","bthg"], "không":["k","K","ko","k0","kO","Ko","khong","kh","khg","hok","hk"], 
              "rồi":["r", "R"], "anh":["a","A"], "mình":["mk","Mk"], "vậy":["z","Z","v","V"], "gì":["j","J","ji"],"trước":["trc"],
              "đi":["ik"], "mọi người": ["mng","Mng","mn","Mn"],"giáo viên":["gv"],"thích":["thix"], "được":["đc","Đc","dc"]}
celeb_dict = {"Trấn Thành": ["xìn","Xìn","TT","tt","Tran Thanh","Tran thanh"], 
              "Phan Mạnh Quỳnh": ["pmq", "PMQ", "phan manh quynh"]}
en_dict = {"trailer": ["traler"], "porn":["pỏn","Pỏn"], "free":["fre"], "full":["ful"], "facebook":["facebok"]}

def create_norm_dict(input_dict):
  norm = {}
  for key, values in input_dict.items():
    for value in values:
      norm[value] = key
  return norm

def normalize(text, words):
  regex = r"\b(?:" + "|".join(re.escape(word) for word in words) + r")\b"
  reobj = re.compile(regex, re.I)
  try:
    res = reobj.sub(lambda x:words[x.group(0)], text)
  except Exception as e:
    res = text
  return res

bag_dicts = {}
for d in (slang_dict,celeb_dict,en_dict): 
  bag_dicts.update(d)
norm_dict = create_norm_dict(bag_dicts)
print(norm_dict)

"""## Split and Demoji into normal words"""

import emoji
import functools
import operator

def split_demoji(text):
  em_split_emoji = emoji.get_emoji_regexp().split(text)
  em_split_whitespace = [substr.split() for substr in em_split_emoji]
  em_split = functools.reduce(operator.concat, em_split_whitespace)
  return emoji.demojize(' '. join(em_split))

# test
# split_demoji(df["comment"][215])

"""## Remove punctuations and special characters with Regex"""

def remove_punc(text):
  text = text.replace('\n', ' ')
  text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,“”'‘’]", ' ', text)
  return text

"""# Preprocess with the following steps

*   Step 1: Replace all links (http[s]://...) and timestamp (1:05, 2:08)
*   Step 2: Normalize text for some specific cases (ko, k --> không, bth, bt --> bình thường, ...)
*   Step 3: Split and demoji (❤️❤️❤️ --split into--> ❤️ ❤️ ❤️ --demoji--> :heart: :heart: :heart:)
*   Step 4: Remove continuous duplicate words within text (hay quá điiiiiiiii)
*   Step 5: Remove punctuations and special characters
*   Step 6: Tokenize words



"""

import itertools
from underthesea import word_tokenize

tokenize_list = []

def preprocess(text):
  # Replace all links and timestamp
  text = re.sub('http[s]?://\S+', '', text)
  text = re.sub(r"([\d{1,2}:\d{2}(:\d{2})?])", ' ', text)

  # Normalize
  text = normalize(text, norm_dict)

  # Demojize
  text = split_demoji(text)

  # Process continuous duplicate words within text
  text = ''.join(i for i, _ in itertools.groupby(text))

  # Remove punctuations and special characters
  text = remove_punc(text)

  # word tokenize
  tokens = word_tokenize(text)
  tokenize_list.append(tokens)

  return ' '.join(tokens).lower()

# test preprocess
# test_text = df["comment"][210]
# preprocess_text(test_text)

import numpy as np

processed_text = []
for comment in df["comment"]:
  processed_text.append(preprocess(comment))
  
df['tokenize'] = np.array(tokenize_list)
df['preprocessed'] = np.array(processed_text)
df.head()

"""# Run Logistic Regression with Pipelines



"""

import unidecode
from sklearn.base import BaseEstimator, TransformerMixin

class RemoveTone(BaseEstimator, TransformerMixin):
    def remove_tone(self, s):
        return unidecode.unidecode(s)

    def transform(self, x):
        return [self.remove_tone(s) for s in x]

    def fit(self, x, y=None):
        return self

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.svm import SVC

X_train, X_test, y_train, y_test = train_test_split(df["preprocessed"], df[SENTIMENT_COLUMN_NAME], test_size=0.2, random_state=42)
pipe = Pipeline(steps=[
            ('features', FeatureUnion([
                ('lower_pipe', Pipeline([
                    ('tfidf', TfidfVectorizer(ngram_range=(1, 4), min_df=2))])),
                ('with_tone_char', TfidfVectorizer(ngram_range=(1, 6), min_df=2, analyzer='char')),
                ('remove_tone', Pipeline([
                    ('remove_tone', RemoveTone()),
                    ('tfidf', TfidfVectorizer(ngram_range=(1, 4), min_df=2))])),
            ])),
            ('estimator', LogisticRegression()),
])

pipe.fit(X_train, y_train)

# Predict on train & test
pred_train = pipe.predict(X_train)
pred_test = pipe.predict(X_test)

# Evaluate on train & test
score_train = pipe.score(X_train, y_train)
score_test = pipe.score(X_test, y_test)
print("Score on train", score_train)
print("Score on test", score_test)

"""# Compare and Export results on Train & Test"""

import os

output_path = f"{path}/output"
if not os.path.exists(output_path):
    os.makedirs(output_path)

df.to_excel(f"{output_path}/logistic_processed.xlsx", sheet_name='processed')
print(f"Please find the output files in path={output_path}")

def create_export_df(comment, sentiment, pred):
  export_df = pd.DataFrame()
  export_df[COMMENT_COLUMN_NAME]=np.array(comment)
  export_df[SENTIMENT_COLUMN_NAME]=np.array(sentiment)
  export_df['pred']=np.array(pred)
  export_df["wrong_pred"] = np.where(export_df[SENTIMENT_COLUMN_NAME] != export_df['pred'], True, False)
  return export_df

train_df = create_export_df(X_train, y_train, pred_train)
train_df.to_excel(f"{output_path}/logistic_train.xlsx", sheet_name='train')

train_df[train_df["wrong_pred"]==True]

test_df = create_export_df(X_test, y_test, pred_test)
test_df.to_excel(f"{output_path}/logistic_test.xlsx", sheet_name='test')

test_df[test_df["wrong_pred"]==True]

"""# Issue notes
- normalize dấu mũ
- boost thêm những từ quan trọng
- should remove celeb name? -> phim này khen nhưng phim khác chê -> tùy vào lượng cmt mà ra kết quả
- xem phim xong trích câu trong truyện -> label tích cực?
- một vài cmt tiếng anh ko đủ data để học
"""