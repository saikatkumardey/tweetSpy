# -*- coding: utf-8 -*-
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
import pika
import time
import sys
from config import config
from keywords import Keywords

keywordObj = Keywords(['python','javascript'])

#Variables that contains the user credentials to access Twitter API
access_token = config['access_token']
access_token_secret = config['access_token_secret']
consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']


class TweetProducer(StreamListener):

    def __init__(self,api):

        self.api = api
        super(StreamListener, self).__init__()

        #setup rabbitMQ Connection
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()

        #set max queue size
        args = {"x-max-length": 2000}

        self.channel.queue_declare(queue='twitter_stream', arguments=args)

    def on_status(self, status):

        if hasattr(status,'retweeted_status'):
            print "it's a retweet"
            return True

        tweet = extract_useful_fields(status)
        #queue the tweet
        print "> ",tweet['text'], tweet.get('place'),tweet.get('coords'),tweet.get('user_location')
        
        self.channel.basic_publish(exchange='',
                                   routing_key='twitter_stream',
                                   body=json.dumps(tweet))
        return True

    def on_error(self, status_code):
        print sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print sys.stderr, 'Timeout...'
        return True  # Don't kill the stream



def extract_useful_fields(status):
    """
    given a json representing a tweet, grab and return data of interest
    """

    tweet = {}
    tweet['text'] = status.text.encode('utf-8')
    tweet['created_at'] = time.mktime(status.created_at.timetuple())
    tweet['geo'] = status.geo
    tweet['coords'] = status.coordinates
    try:
        tweet['place'] = status.place.country
        tweet['user_location'] = status.user.location
    except Exception as e:
        tweet['place'] = None
        tweet['user_location'] = None
    tweet['user'] = status.user.name

    return tweet


def run_stream(interval=300):

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    
    twitter_stream = Stream(auth, TweetProducer(api))

    while True:
        
        if twitter_stream.running is True:
            twitter_stream.disconnect()

        keywords = keywordObj.get_keywords()

        if keywords == []:
            print "No keywords provided"
        else:
            try:
                twitter_stream.filter(track=keywords,async=False)
            except Exception as e:
                print "error"

        time.sleep(interval)



if __name__ == '__main__':

    print("streaming started")
    run_stream()
    # sapi = Stream(auth, TweetProducer(api))
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # sapi.filter(track=['python','machine learning','data science','deep learning'],async=True)
    # run_stream(sapi,300)
