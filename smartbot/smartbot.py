#!/usr/bin/python3

from secret import *
import tweepy
import recastai
import json
from SparkConnector.sparkConnect import sparkconnector


class twitter_bot(tweepy.StreamListener):

    def __init__(self):
        self.auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        self.auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.sparkroom = sparkconnector()
        self.currentTopic = {}

    def sendTweet(self, text):
        try :
            self.api.update_status(text)
        except :
            print('last request has bee ignored : Duplicate Tweet')
            pass

    def pushInstanceAndTextToRecast(self,recastInstance, text):
        return recastInstance.text_converse(text)


    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        if decoded['user']['screen_name'] != "SmartParisBot":
            print(decoded['text'])
            print(decoded['text'][15:])
            if decoded['user']['screen_name'] in self.currentTopic.keys() :
                currentInstance = self.currentTopic[decoded['user']['screen_name']]
                Answer = self.pushInstanceAndTextToRecast(currentInstance,decoded['text'][15:])
                print(Answer.reply())
                print(Answer.next_action())
                try :
                    self.sendTweet('@' + decoded['user']['screen_name'] + " " + Answer.reply())
                except :
                    self.sendTweet('@' + decoded['user']['screen_name'] + " " + "je suis à l'agonie")
            else :
                self.currentTopic[decoded['user']['screen_name']] = recastLink = recastai.Client(token=R_TOKEN, language='fr')
                currentInstance = self.currentTopic[decoded['user']['screen_name']]
                Answer = self.pushInstanceAndTextToRecast(currentInstance,decoded['text'][15:])
                print(Answer.reply())
                print(Answer.next_action())
                try :
                    self.sendTweet('@' + decoded['user']['screen_name'] + " " + Answer.reply())
                except :
                    self.sendTweet('@' + decoded['user']['screen_name'] + " " + "je suis à l'agonie")

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        self.sparkroom.sendToRoom('@%s: %s' % (decoded['user']['screen_name'],
                           self.cleanTweettext(decoded['text']).encode('UTF-8', 'ignore')))
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
        stream.filter(track=['@SmartParisBot'], async=True)


if __name__ == "__main__":

    bot = twitter_bot()
    #bot.sendTweet("Bonjour à tous ! Mon troisième bottweet !")
    bot.startBot()
