import tweepy
import random
import json
import config
from textblob import TextBlob
import matplotlib.pyplot as plt
import streamlit as st
import requests
import streamlit.components.v1 as components


class get_html_tweet(object):
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = "https://publish.twitter.com/oembed?url={}".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=600)

def authenticate():
  client  = tweepy.Client(bearer_token = config.BEARER_TOKEN,
                          consumer_key = config.CONSUMER_KEY,
                          consumer_secret = config.CONSUMER_KEY,
                          access_token = config.ACCESS_TOKEN,
                          access_token_secret = config.ACCESS_TOKEN_SECRET)
  return client

def get_tweets(query, number_of_tweets):
  global tweets_list 
  tweets_list = []
  positive, negative, neutral, polarity = 0,0,0,0
  client = authenticate()
  tweets = client.search_recent_tweets(query = query, max_results = 100)
  tweet_data = tweets.data
  global tweet_link_example
  tweet_link_example = '' 
  

  for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
                              tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=number_of_tweets):
    x = tweet
    analysis = TextBlob(tweet.text)
    polarity += analysis.sentiment.polarity

    if(analysis.sentiment.polarity == 0):
      neutral += 1
    elif(analysis.sentiment.polarity < 0.00):
      negative += 1
    elif(analysis.sentiment.polarity > 0.00):
      positive += 1
    tweets_list.append(tweet.text)

  tweet_link_example = f"https://twitter.com/user/status/{tweet.id}"
  
  return positive, negative, neutral


st.title("Stock Prediction using Twitter Sentiment Analysis Web App")
st.subheader("""Twitter sentiment analysis web application developed for **Software Engineering** project 2021-2022""")
st.markdown('##')

st.write("""**Enter the name of the stock/financial asset you would like to check the sentiment of in real time.**""")
keyword = st.text_input("Keyword", 'Bitcoin')
st.write("""**Enter the number of tweets the Twitter API should extract concerning the specific keyword.**""")
number_of_tweets = st.slider('Number of Tweets', min_value=100, max_value=500, value=100, step=30)
result = st.button("Analyze")

if(result):
  pos, neg, neu = get_tweets(keyword, number_of_tweets)

  labels  = ['Positive','Neutral','Negative']
  sizes = [pos, neu, neg]
  fig1, ax1 = plt.subplots()
  ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
          shadow=True, startangle=90, colors = ['#31333F', '#F0F2F6', '#FF4B4B'])
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  st.pyplot(fig1)
  st.subheader("Extracted Tweet Example")
  t = get_html_tweet(tweet_link_example).component()