from flask import Flask, render_template
from my_package.model import predict_on_twitter_data 

app = Flask(__name__)

@app.route('/')
def hello():
    df = predict_on_twitter_data("blockchain")
    json = df.to_json()
    return json