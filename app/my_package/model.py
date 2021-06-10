import numpy as np
import pickle
from keras import models    
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
from .twitter import get_tweet_dataframe 


def load_model():
# loading
    with open('../tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    model = models.load_model("../model")

    return tokenizer, model

def predict_on_twitter_data(keyword, no_of_tweets=100):
    tokenizer, model = load_model()

    df = get_tweet_dataframe(keyword, no_of_tweets)

    data = df['text']
    data = tokenizer.texts_to_sequences(data)
    data = pad_sequences(data, maxlen=33)
    ypred = model.predict(data)

    prediction = []
    for pred in ypred:
        prediction.append(np.argmax(pred))

    df['prediction'] = prediction

    return df