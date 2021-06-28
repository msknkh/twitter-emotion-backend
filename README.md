## About this repository :-

This repository contains the backend api in flask for fetching the tweets for a certain keyword or hashtag from twitter api and then using a saved LSTM model that I trained to classify tweets into 7 emotion categories namely: anger, disgust, fear, sadness, joy, neutral and surprise. 

The model obtained accuracy of 73% by fine tuning bert model and accuracy of 63% by training LSTM model. The training was performed on GoEmotions dataset. 

## To run the flask server :-

After cloning the repository and entering the repository folder :-

1. Create a virtual environment using the command
```
python3 -m venv env
```

2. Enter the virtual environment
```
source env/bin/activate
```

3. Export your Bearer Token for twitter api
```
export BEARER_TOKEN = "********************"
```

4. Install the dependencies
```
pip3 install -m requirements.txt
```

5. Run the app 
```
flask run 
```

The frontend for the project is written in React and is in the repository :- https://github.com/msknkh/twitter-emotion-frontend




