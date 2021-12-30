import tweepy
import random
import json
import config
from textblob import TextBlob
import matplotlib.pyplot as plt
import streamlit as st

st.write('Hello')
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

  positive = format(percentage(positive, number_of_tweets), '.2f')
  negative = format(percentage(negative, number_of_tweets), '.2f')
  neutral = format(percentage(neutral, number_of_tweets), '.2f')
  
  return positive, negative, neutral

keyword = input("Enter the keyword to search for: ")
number_of_tweets = int(input("Enter the number of tweets to search for: "))
pos, neg, neu = get_tweets(keyword, number_of_tweets)

labels  = ['Positive ['+str(pos)+'%]','Neutral ['+str(neu)+'%]','Negative ['+str(neg)+'%]']
sizes = [pos, neu, neg]
colors = ['yellowgreen', 'gold', 'red']
patches, texts = plt.pie(sizes, colors = colors)
plt.legend(patches, labels, loc = 'best')
plt.title("Sentiment Analysis")
plt.axis('equal')
plt.tight_layout()
plt.show()