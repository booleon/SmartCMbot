################################################################
## Hackathon Bemyapp: City'zen Bots Cisco 
## Equipe: SmartParisBot
## Interface SMS <->Tropo <-> Recast.AI
## Script by @pedrosimao -10/12/2016
################################################################
import urllib, requests, json
from itty import *
from tropo import Tropo,Result,Session
import base64

##############
## Function adds users infos to Database
##############
def userswaiting(numero, what, place) :
	# Empty dict
	the_users = {}
	# Fill in the entries one by one
	the_users["numero"] = numero
	the_users["type"] = what
	the_users["place"] = place
	with open('userswaiting.json', 'w') as fp:
		json.dump(the_users, fp)

##############
## Function that creates a JSON for Converse
##############
def startconverse(the_json) :
	with open('converse.json', 'w') as fp:
		json.dump(the_json, fp)
		print("<<<< Internal Json Created >>>>")
		print(the_json)

##############
## Function that ends JSON conversation
##############
def endconverse() :
	with open('converse.json', 'w') as fp:
		json.dump(" ", fp)

##############
## Function that opens OLD conversation
##############
def openconverse() :
	with open('converse.json') as json_data:
		d = json.load(json_data)
		print(d)

@post('/index.json')
def index(request):
	s = Session(request.body)
	initialText = s.initialText
	#callerID = s.fromaddress['id']
	callerID = "+33685651240"
	print(callerID)
	headers = {'Authorization': 'Token 3da836038be5fb570158829ae76d3aeb'}
	t = Tropo()
	url = 'https://api.recast.ai/v2/converse'
	with open('converse.json') as json_data:
		conv = json.load(json_data)
	#conToken = conv["results"]["conversation_token"]
	#print("<<<< conToken opened >>>>")
	#print(conToken)


	# Test Echo
	if(initialText == "This is an echo.") :
		t.call(to=callerID, network = "SMS")
		gotEcho = "J'ai recu votre echo!'"
		t.say(gotEcho)
		# Send echo confirmation
		res = requests.get('https://api.tropo.com/1.0/sessions?action=create&token=516b787555467055586f63625a754270414e714264506b704c715a6e7578575474545051745a4175676d7177&cNumber=' + callerID + '&cAnswer=' + gotEcho)

	# #Conversation already started
	# elif (conToken != "0") :
	# 	replyload = {'conversation_token': conToken}
	# 	bresponse = requests.put('https://api.recast.ai/v2/converse',json=replyload, headers=headers)
	# 	print (bresponse)
	# 	# Finish conversation
	# 	endconverse()

	#This is a new conversation
	else :
		# This one create a new JSON
		#userswaiting(callerID, initialText, "Place de la Nation")
		payload = {'text': initialText,'language': 'fr'}
		response = requests.post(url, json=payload, headers=headers)
		#In case we get an answer from Recast.AI
		if response : 
			# Create a local copy of the json
			my_json = json.loads(response.text)
			#print all
			print("<<<< External Json Recieved >>>>")
			print(my_json) 
			startconverse(my_json)
			#Bot reply
			breply = my_json["results"]["replies"][0]
			print(breply)
			# Send reply to SMS via API
			res = requests.get('https://api.tropo.com/1.0/sessions?action=create&token=516b787555467055586f63625a754270414e714264506b704c715a6e7578575474545051745a4175676d7177&cNumber=' + callerID + '&cAnswer=' + str(breply))
			# Get conversation token
			conToken = my_json["results"]["conversation_token"]
			print("<<<< conToken created >>>>")
			print(conToken)
			startconverse(my_json)

	return t.RenderJson()
	
# @post("/continue")
# def index(request):
# 	r = Result(request.body)
# 	t = Tropo()
# 	answer = r.getValue()
# 	if (answer == "car"):
# 		t.say ("You have chosen car.")
# 	userswaiting("+33666666", answer, "Place de la la la")
# 	return t.RenderJson()
	
run_itty(server='wsgiref', host='localhost', port=8080)