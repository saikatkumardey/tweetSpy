# -*- coding: utf-8 -*-
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
import preprocessor as tweet_preprocessor
import re
import redis
import pandas as pd

class Analytics():

    def __init__(self):
        self.tb = Blobber()
        self.db = redis.Redis('localhost')
        self.count_dictname = "sentiment"
        self.db.hmset(self.count_dictname,{'positive':0,'negative':0})

    def preprocess(self,text):
        text = text.encode('utf-8')
        text = tweet_preprocessor.clean(text)
        word_list = re.findall("[\w]+",text)
        return word_list

    def get_sentiment(self,text):

        word_list = self.preprocess(text)
        cleaned_sentence = ' '.join(word_list)

        senti = self.tb(text)
        senti_type = 'positive' if senti.polarity > 0 else 'negative'

        return {'sentiment': senti_type}

    def get_sentiments_bulk(self,text_list=None):

        data = []

        if text_list is None: 
            return data
        else:
            data = [self.get_sentiment(text) for text in text_list]

        return data

    def update_sentiment_count(self,count):

        latest_count = self.get_latest_count()

        for k,v in count.items():
            latest_count[k] = int(latest_count[k]) + int(v)

        print latest_count

        self.db.hmset(self.count_dictname,latest_count)


    def get_latest_count(self):

        return self.db.hgetall(self.count_dictname)


    def count_sentiment_types(self,tweets):

        df = pd.DataFrame(tweets)
        count = df.sentiment.value_counts(tweets).to_dict()
        return count


    def get_tweet_sentiments(self,tweets):

        tweet_texts = [t.get('text') for t in tweets]
        sentiments = self.get_sentiments_bulk(tweet_texts)
        for idx,item in enumerate(sentiments):
            print idx,item,tweet_texts[]
            tweets[idx]['sentiment'] = item['sentiment']

        return tweets

    def run_sentiment_analysis(self,tweets):

        tweets_with_sentiments = self.get_tweet_sentiments(tweets)

        count = self.count_sentiment_types(tweets_with_sentiments)

        self.update_sentiment_count(count)

        latest_count = self.get_latest_count()

        return latest_count







