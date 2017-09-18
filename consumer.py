# -*- coding: utf-8 -*-
import pika
import json
import time

class TweetConsumer():

    def __init__(self):

        connection = pika.BlockingConnection()
        self.channel = connection.channel()

    #function to get X messages from the queue
    def get_tweets(self,size=10):
        tweets = []
        count = 0
        for method_frame, properties, body in self.channel.consume('twitter_stream'):

            tweets.append(json.loads(body))
            count += 1

            # Acknowledge the message
            self.channel.basic_ack(method_frame.delivery_tag)

            # Escape out of the loop after 10 messages
            if count == size:
                break

        # Cancel the consumer and return any pending messages
        requeued_messages = self.channel.cancel()
        print 'Requeued %i messages' % requeued_messages

        return tweets
