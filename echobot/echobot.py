#!/usr/bin/python3

from secret import *
import tweepy
import json

class echobot(tweepy.StreamListener) :
    def __init__(self) :
        self.auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        self.auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

    def sendTweet(self,text) :

        self.api.update_status(text)

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        self.sendTweet('%s' % (decoded['text'].encode('ascii', 'ignore')))
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print ('@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))
        print ('')
        return True

    def on_error(self, status):
        print (status)

    def startBot (self) :
        print ("Showing all tweets I will resend :")
        stream = tweepy.Stream(self.auth, self)
        stream.filter(track=['@smartparisbot'],async=True)


if __name__ == "__main__" :

    bot = echobot()
    #bot.sendTweet("Bonjour à tous ! Mon troisième bottweet !")
    bot.startBot()