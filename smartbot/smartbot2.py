#!/usr/bin/python3

from secret import *
import tweepy
import json
from SparkConnector.sparkConnect import sparkconnector
import requests


class twitter_bot(tweepy.StreamListener):

    def __init__(self):
        self.auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        self.auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.sparkroom = sparkconnector()

        self.activUsers = {}

    def sendTweet(self, text):
        try :
            self.api.update_status(text)
        except :
            print('last request has been ignored : Duplicate Tweet')

    def startGetMyFuckingData(self, token, text) :
        response = requests.post('https://api.recast.ai/v2/converse',
            json={'text': text,'language': 'fr'},
            headers={'Authorization': 'Token ' + token})
        rep = response.text
        dico = json.loads(rep)
        return dico

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        print('@' + decoded['user']['screen_name'] + ' : ' + decoded['text'])
        if decoded['user']['screen_name'] != "SmartParisBot":
            if decoded['user']['screen_name'] not in self.activUsers.keys() :
                self.activUsers[decoded['user']['screen_name']] = {}
                self.sendTweet('@' + decoded['user']['screen_name'] + ' ' + self.askRecast(decoded['user']['screen_name'],decoded['text']))
                print('@' + decoded['user']['screen_name'] + ' ' + self.askRecast(decoded['user']['screen_name'],decoded['text']))
            else :
                self.sendTweet('@' + decoded['user']['screen_name'] + ' ' + self.askRecast(decoded['user']['screen_name'],decoded['text']))
                print('@' + decoded['user']['screen_name'] + ' ' + self.askRecast(decoded['user']['screen_name'],decoded['text']))

                # self.activUsers[decoded['user']['screen_name']]['data_loc'] = None
                # self.activUsers[decoded['user']['screen_name']]['data_time'] = None
                # self.activUsers[decoded['user']['screen_name']]['data_topic'] = None
                # self.activUsers[decoded['user']['screen_name']]['data_transport'] = None
                # self.activUsers[decoded['user']['screen_name']]['data_hello'] = None



    def askRecast(self,user,text) :
        hello = self.startGetMyFuckingData(GREETINGS, text[15:])
        topic = self.startGetMyFuckingData(QUESTION, text[15:])
        loc = self.startGetMyFuckingData(TIME_LOC, text[15:])
        time = loc

        try :
            self.activUsers[user]['data_hello'] = hello['results']['replies']
        except :
            pass
        try :
            self.activUsers[user]['data_topic'] = topic['results']['entities']['keyword'][0]['value']
        except :
            pass
        try :
            self.activUsers[user]['data_loc'] = loc['results']['memory']['location']
        except :
            pass
        try :
            self.activUsers[user]['data_time'] = loc['results']['memory']['timestamp']
        except :
            pass

        if 'data_topic' not in self.activUsers[user].keys() :
            if 'data_hello' not in self.activUsers[user].keys() :
                return "Je n'ai pas compris votre demande"
            else :
                return self.activUsers[user]['data_hello'][0]
        elif 'location' in self.activUsers[user].keys() and 'timestamp' in self.activUsers[user].keys() :
            #@Cedric
            pass
        else :
            return "Quand et où s'il vous plait ?"








        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        self.sparkroom.sendToRoom('@%s: %s' % (decoded['user']['screen_name'],
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
