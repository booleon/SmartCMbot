#!/usr/bin/python3

import requests
from secret import *

url = "https://api.ciscospark.com/v1/messages"

payload = "{\r\n  \"toPersonEmail\" : \"cedric.bonhomme@metapolis.fr\",\r\n  \"text\" : \"This message is sent to a person directly => will create a 1-1 room, and make you rejoin a pre-existing 1-1 room you've chosen to leave\"\r\n}"
headers = {
    'authorization': "Bearer " + SPARK_DEV_KEY + "",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token':  POSTMAN_KEY
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
