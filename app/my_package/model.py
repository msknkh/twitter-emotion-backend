import numpy as np
import pickle
from keras import models    
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
from .twitter import get_tweet_dataframe 
import os

'''
def load_model():
    
    # absolute path to this file
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    # absolute path to this file's root directory
    PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 
    path_tokenizer = os.path.join(FILE_DIR, 'tokenizer.pickle')
    path_model = os.path.join(FILE_DIR, 'model')


    # loading
    with open(path_tokenizer, 'rb') as handle:
        tokenizer = pickle.load(handle)

    model = models.load_model(path_model)

    return tokenizer, model
'''

def predict_on_twitter_data(keyword, no_of_tweets=100):

    # absolute path to this file
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    # absolute path to this file's root directory
    PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 
    path_tokenizer = os.path.join(FILE_DIR, 'tokenizer.pickle')
    path_model = os.path.join(FILE_DIR, 'mymodel.h5')

    # loading
    with open(path_tokenizer, 'rb') as handle:
        tokenizer = pickle.load(handle)

    model = models.load_model(path_model)

    df = get_tweet_dataframe(keyword, no_of_tweets)

    data = df['text']
    data = tokenizer.texts_to_sequences(data)
    data = pad_sequences(data, maxlen=33)
    ypred = model.predict(data)

    prediction = []
    for pred in ypred:
        prediction.append(np.argmax(pred))

    df['prediction'] = prediction

    json = df.to_json()
    return json