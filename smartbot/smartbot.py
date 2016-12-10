#!/usr/bin/python3

from secret import *
import tweepy
import recastai
import json


class twitter_bot(tweepy.StreamListener):

    def __init__(self):
        self.auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        self.auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.client = recastai.Client(token=R_TOKEN, language='en')

    def sendTweet(self, text):
        self.api.update_status(text)

    def do_somethingsmart(self, text):
        response = self.client.text_converse(text)
        reply = response.reply()
        print(reply)
        self.sendTweet(reply)

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        if decoded['user']['screen_name'] != "SmartParisBot":
            self.do_somethingsmart(decoded['text'])
            # pass
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print('@%s: %s' % (decoded['user']['screen_name'],
                           self.cleanTweettext(decoded['text']).encode('UTF-8', 'ignore')))
        print('')
        return True

    def cleanTweettext(self, text):
        return str(text[2:-1])

    def on_error(self, status):
        print(status)

    def startBot(self):
        print("Showing all tweets I will resend :")
        stream = tweepy.Stream(self.auth, self)
        stream.filter(track=['SmartParisBot'], async=True)


if __name__ == "__main__":

    bot = twitter_bot()
    #bot.sendTweet("Bonjour à tous ! Mon troisième bottweet !")
    bot.startBot()
