from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
import pika
import time
import sys

from config import config


#Variables that contains the user credentials to access Twitter API
access_token = config['access_token']
access_token_secret = config['access_token_secret']
consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)



def extract_useful_fields(status):
    """
    given a json representing a tweet, grab and return data of interest
    """

    fields = ['coordinates','created_at','entities','id_str','place','text','user']

    tweet = {}
    tweet['text'] = status.text
    tweet['created_at'] = time.mktime(status.created_at.timetuple())
    tweet['geo'] = status.geo
    tweet['place'] = status.place
    tweet['user'] = status.user.name

    return tweet


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

        tweet = extract_useful_fields(status)
        #queue the tweet
        print "> ",tweet['text']
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



if __name__ == '__main__':

    sapi = Stream(auth, TweetProducer(api))
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    sapi.filter(track=['python','machine learning','data science','deep learning'],async=True)
