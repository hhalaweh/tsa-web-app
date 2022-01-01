import tweepy
import random
import json
import config
from textblob import TextBlob
import matplotlib.pyplot as plt
import streamlit as st

st.write("""# Twitter Sentiment Analysis App""")

def authenticate():
  client  = tweepy.Client(bearer_token = config.BEARER_TOKEN,
                          consumer_key = config.CONSUMER_KEY,
                          consumer_secret = config.CONSUMER_KEY,
                          access_token = config.ACCESS_TOKEN,
                          access_token_secret = config.ACCESS_TOKEN_SECRET)
  return client

def percentage(part, whole):
  return 100 * float(part)/float(whole)

def get_tweets(query, number_of_tweets):
  global tweets_list 
  tweets_list = []
  positive, negative, neutral, polarity = 0,0,0,0
  client = authenticate()
  tweets = client.search_recent_tweets(query = query, max_results = 100)
  tweet_data = tweets.data
  

  for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
                              tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=number_of_tweets):
    analysis = TextBlob(tweet.text)
    polarity += analysis.sentiment.polarity

    if(analysis.sentiment.polarity == 0):
      neutral += 1
    elif(analysis.sentiment.polarity < 0.00):
      negative += 1
    elif(analysis.sentiment.polarity > 0.00):
      positive += 1
    tweets_list.append(tweet.text)

  #positive = format(percentage(positive, number_of_tweets), '.2f')
  #negative = format(percentage(negative, number_of_tweets), '.2f')
  #neutral = format(percentage(neutral, number_of_tweets), '.2f')
  
  return positive, negative, neutral
st.write("""### Here you can enter the keyword you would like to check the sentiment of in real time.""")
keyword = st.text_input("Keyword", 'Bitcoin')
st.write("""### Here you can enter the number of tweets the Twitter API should extract concerning the specific keyword.""")
number_of_tweets = st.slider('Number of Tweets', min_value=100, max_value=500, value=100, step=30)
result = st.button("Analyze")

if(result):
  pos, neg, neu = get_tweets(keyword, number_of_tweets)

  labels  = ['Positive ['+str(pos)+'%]','Neutral ['+str(neu)+'%]','Negative ['+str(neg)+'%]']
  sizes = [pos, neu, neg]
  fig1, ax1 = plt.subplots()
  ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
          shadow=True, startangle=90)
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  st.pyplot(fig1)