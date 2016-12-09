#!/usr/bin/python3

import tweepy
import json

# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = '46EKaD26rYQIporc1axXZIKeM'
consumer_secret = 'u8XADqMVdi7VKPPYKVRwx8leiTI0bQTOQPL5QkJmKFm4PPrWQZ'
access_token = '806851098258657280-r5SaqdZsd2cBSkr82ggkZOOIoreDxaR'
access_token_secret = '5HJYxQK4E7CQtrw2lIt9OI4fJS19A9umwlnBHK0UCEKpF'

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print ('@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))
        print ('')
        return True

    def on_error(self, status):
        print (status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print ("Showing all new tweets for #programming:")

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['@smartparisbot'],async=True)
