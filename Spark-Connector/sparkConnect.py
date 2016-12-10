#!/usr/bin/python3

import requests
import json
from secret import *
from ciscosparkapi import CiscoSparkAPI

class sparkconnector :

    def __init__(self, mykey=SPARK_DEV_KEY) :
        api = CiscoSparkAPI(access_token=mykey)
        decoded = json.loads(api.people.me())
        print("now connected as" + decoded['displayName'])
