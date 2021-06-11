import emoji
from bs4 import BeautifulSoup
import requests
import os
import json
import re
import pandas as pd

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = str(os.getenv("BEARER_TOKEN")) 

def clean_text(text):
    '''Clean emoji, Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''
    text = emoji.demojize(text)
    text = re.sub(r'\:(.*?)\:','',text)
    text = str(text).lower()    #Making Text Lowercase
    text = re.sub('\[.*?\]', '', text)
    #The next 2 lines remove html text
    text = BeautifulSoup(text, 'lxml').get_text()
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub(r'#(\w+)', '', text)
    text = re.sub(r'_(\w+)', '', text)
    # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",", "'")
    #text = re.sub(r"[^a-zA-Z?.!,¿']+", " ", text)
    return text


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(search_url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def clean_tweet(tweet):
    '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())


def get_tweets(keyword, no_of_tweets):
    
    search_url = "https://api.twitter.com/2/tweets/search/recent"

    headers = create_headers(bearer_token)

    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query_params = {'tweet.fields': 'author_id,created_at,public_metrics',
                'expansions': 'author_id',
                'user.fields': 'public_metrics',
                'max_results': 100}
    query_params['query'] = "({k} -is:retweet lang:en) OR (#{k} lang:en -is:retweet)".format(k=keyword)

    json_response = connect_to_endpoint(search_url, headers, query_params)

    text = []
    tweet_id = []
    retweet_count = []
    followers_count = []
    like_count = []
    
    user_dict = {}
    
    for user in json_response['includes']['users']:
        user_id = user['id']
        followers_co = user['public_metrics']['followers_count']
        user_dict[user_id] = followers_co

    for tweet in json_response['data']:
        tweet_clean = clean_tweet(tweet['text'])
        tweet_clean = clean_text(tweet_clean)
        text.append(tweet_clean)
        tweet_id.append(tweet['id'])
        retweet_count.append(tweet['public_metrics']['retweet_count'])
        followers_count.append(user_dict[tweet['author_id']])
        like_count.append(tweet['public_metrics']['like_count'])

    for i in range(1, no_of_tweets%100):
        print("hello")
        next_tok= json_response['meta']['next_token']
        query_params['next_token'] = next_tok
        json_response = connect_to_endpoint(search_url, headers, query_params)
        

        for user in json_response['includes']['users']:
            user_id = user['id']
            followers_co = user['public_metrics']['followers_count']
            user_dict[user_id] = followers_co

        for tweet in json_response['data']:
            tweet_clean = clean_tweet(tweet['text'])
            tweet_clean = clean_text(tweet_clean)
            text.append(tweet_clean)
            tweet_id.append(tweet['id'])
            retweet_count.append(tweet['public_metrics']['retweet_count'])
            followers_count.append(user_dict[tweet['author_id']])
            like_count.append(tweet['public_metrics']['like_count'])

    return text, tweet_id, retweet_count, followers_count, like_count

def get_tweet_dataframe(keyword, no_of_tweets):

    text, tweet_id, retweet_count, followers_count, like_count = get_tweets(keyword, no_of_tweets)
    combined_popularity_count = []
    for i in range(len(followers_count)):
        combined_popularity_count.append(followers_count[i] + 10*like_count[i] + 10*retweet_count[i])

    df = pd.DataFrame(list(zip(tweet_id, text, combined_popularity_count)),
                      columns=['tweet_id', 'text', 'combined_popularity_count'])
    df = df.sort_values('combined_popularity_count', ascending=False)

    return df