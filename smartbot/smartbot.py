#!/usr/bin/python3

from secret import *
import tweepy
import recastai
import json
from SparkConnector.sparkConnect import sparkconnector
import requests


class twitter_bot(tweepy.StreamListener):

    def __init__(self):
        self.auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        self.auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.sparkroom = sparkconnector()
        self.currentTopic = {}
        self.recastLink = recastai.Client(token=R_TOKEN, language='fr')

    def sendTweet(self, text):
        try:
            self.api.update_status(text)
        except:
            print('last request has been ignored : Duplicate Tweet')

    def startGetMyFuckingData(self, text):
        response = requests.post('https://api.recast.ai/v2/converse',
                                 json={'text': text, 'language': 'fr'},
                                 headers={'Authorization': 'Token ' + R_TOKEN})
        rep = response.text
        print('pour le plaisir, ce que je récupère : ')
        print(rep)
        dico = json.loads(rep)
        print('pour le plaisir, le dictionnaire : ')
        print(dico)
        return dico

    def getMyFuckingData(self, recastaiKey, answerKey):
        response = requests.put('https://api.recast.ai/v2/converse',
                                json={'conversation_token': answerKey},
                                headers={'Authorization': 'Token ' + recastaiKey})
        rep = response.text
        print('pour le plaisir, ce que je récupère : ')
        print(rep)
        dico = json.loads(rep)
        print('pour le plaisir, le dictionnaire : ')
        print(dico)
        return dico

    def pushInstanceAndTextToRecast(self, text, conversationID=None):
        if conversationID is None:

            return self.recastLink.text_converse(text)
        else:
            return self.recastLink.text_converse(text, conversation_token=conversationID)

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        print('@' + decoded['user']['screen_name'] + ' : ' + decoded['text'])
        if decoded['user']['screen_name'] != "SmartParisBot":
            if decoded['user']['screen_name'] in self.currentTopic.keys():
                currentInstance = self.recastLink
                answer = self.pushInstanceAndTextToRecast(decoded['text'][15:], self.currentTopic[
                                                          decoded['user']['screen_name']])

                # try :
                self.getMyFuckingData(R_TOKEN, self.currentTopic[decoded['user']['screen_name']])
                # except :
                #    print("hé merde")

                if False:

                    tweet = '@' + decoded['user']['screen_name'] + " " + "On a fini, merci :-)"
                    self.sendTweet(tweet)
                    print('answer : ' + tweet)
                else:
                    try:
                        print('answer : ' + answer.reply())
                        self.sendTweet('@' + decoded['user']['screen_name'] + " " + answer.reply())
                    except:
                        self.sendTweet('@' + decoded['user']['screen_name'] + " " +
                                       "Je ne peux plus vous répondre pour le moment, désolé.")
            else:

                currentInstance = self.recastLink
                answer = self.pushInstanceAndTextToRecast(decoded['text'][15:])
                print('test new way of working : ')
                yolo = self.startGetMyFuckingData(decoded['text'][15:])
                print('Encore mieux : ')
                print('')
                print(yolo['results']['uuid'])
                print('')
                self.getMyFuckingData(R_TOKEN, yolo['results']['conversation_token'])
                self.currentTopic[decoded['user']['screen_name']] = answer.conversation_token
                if False:

                    tweet = '@' + decoded['user']['screen_name'] + " " + "On a fini, merci :-)"
                    self.sendTweet(tweet)
                    print('answer : ' + tweet)
                else:
                    print('answer : ' + answer.reply())
                    try:
                        self.sendTweet('@' + decoded['user']['screen_name'] + " " + answer.reply())
                    except:
                        print(answer.get_memory())
                        self.sendTweet('@' + decoded['user']['screen_name'] + " " +
                                       "Je ne peux plus vous répondre pour le moment, désolé.")

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
