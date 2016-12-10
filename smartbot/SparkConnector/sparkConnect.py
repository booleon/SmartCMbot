#!/usr/bin/python3

import requests
import json
from secret import *
from ciscosparkapi import CiscoSparkAPI

class sparkconnector :

    def __init__(self, mykey=SPARK_DEV_KEY) :
        self.api = CiscoSparkAPI(access_token=mykey)
        user = self.api.people.me()
        print("Moderator connected as " + user.displayName)
        self.cleanRooms("smartCMbot_admin")
        print('Old Room removed')
        self.adminroom = self.api.rooms.create("smartCMbot_admin")
        print("Room smartCMbot_admin created")

    def sendToRoom(self, message) :
        self.api.messages.create(self.adminroom.id,text=message)

    def cleanRooms(self, room_name) :
        all_rooms = self.api.rooms.list()
        old_rooms = [room for room in all_rooms if room_name in room.title]

        # Delete all of the demo rooms
        for room in old_rooms:
            self.api.rooms.delete(room.id)

if __name__ == "__main__" :
    connect = sparkconnector()
    connect.sendToRoom('hello world')
