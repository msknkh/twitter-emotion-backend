from flask import Flask, render_template, request
from flask_cors import CORS
import os
import pickle
from keras import models
from twitter import get_tweet_dataframe 
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app, support_credentials=True)

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# absolute path to this file's root directory
PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 
path_tokenizer = os.path.join(FILE_DIR, 'tokenizer.pickle')
path_model = os.path.join(FILE_DIR, 'mymodel.h5')

# loading tokenizer and model 
with open(path_tokenizer, 'rb') as handle:
    TOKENIZER = pickle.load(handle)

MODEL = models.load_model(path_model)

def predict_on_twitter_data(keyword, no_of_tweets=100):

    df = get_tweet_dataframe(keyword, no_of_tweets)

    data = df['text']
    data = TOKENIZER.texts_to_sequences(data)
    data = pad_sequences(data, maxlen=33)
    ypred = MODEL.predict(data)

    prediction = []
    for pred in ypred:
        prediction.append(np.argmax(pred))

    df['prediction'] = prediction

    json = df.to_json()
    return json

@app.route('/')
def hello():
    return "hello"

@app.route('/tweets/', methods=['GET'])
def get_tweets():
    keyword = request.args.get('keyword')
    count_of_tweets = int(request.args.get('count_of_tweets'))
    json = predict_on_twitter_data(keyword, count_of_tweets)
    
    return json

if __name__ == "__main__":
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    # absolute path to this file's root directory
    PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 
    path_tokenizer = os.path.join(FILE_DIR, 'tokenizer.pickle')
    path_model = os.path.join(FILE_DIR, 'mymodel.h5')

    # loading tokenizer and model 
    with open(path_tokenizer, 'rb') as handle:
        TOKENIZER = pickle.load(handle)

    MODEL = models.load_model(path_model)

    app.run(host="0.0.0.0", port="9999")