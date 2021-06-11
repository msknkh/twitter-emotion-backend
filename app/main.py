from flask import Flask, render_template, request
from .my_package.model import predict_on_twitter_data 
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/')
def hello():
    return "hello"

@app.route('/tweets/', methods=['GET'])
def get_tweets():
    keyword = request.args.get('keyword')
    count_of_tweets = int(request.args.get('count_of_tweets'))
    json = predict_on_twitter_data(keyword, count_of_tweets)
    return json