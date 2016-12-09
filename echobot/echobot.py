#!/usr/bin/python3

from secret import *
import tweepy

class echobot :
    def __init__(self) :
        auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def sendTweet(self,text) :

        self.api.update_status(text)

if __name__ == "__main__" :

    bot = echobot()
    bot.sendTweet("Bonjour à tous ! Mon deuxième bottweet !")
