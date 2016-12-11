################################################################
## Hackathon Bemyapp: City'zen Bots Cisco 
## Equipe: SmartParisBot
## Interface SMS <->Tropo <-> Recast.AI
## Script by @pedrosimao -10/12/2016
################################################################

import requests,json
from itty import *
from tropo import Tropo, Result, Session

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

@post('/index.json')
def index(request):
	s = Session(request.body)
	initialText = s.initialText
	t = Tropo()

	if(initialText == "This is an echo.") :
		t.call(to="+33685651240", network = "SMS")
		t.say("Echo well recieved!")
		res = requests.get('https://api.tropo.com/1.0/sessions?action=create&token=516b787555467055586f63625a754270414e714264506b704c715a6e7578575474545051745a4175676d7177&cNumber=+33685651240&cAnswer=IGotTheEcho')
	else :
		userswaiting("+33685651240", initialText, "Place de la Nation 1h18")
		t.call(to="+33685651240", network = "SMS")
		t.say("Message sent to DB!")
		#res = requests.get('https://api.tropo.com/1.0/sessions?action=create&token=516b787555467055586f63625a754270414e714264506b704c715a6e7578575474545051745a4175676d7177&cNumber=+33685651240&cAnswer=SentToDB')
		response = requests.post('https://api.recast.ai/v2/converse',json={'text': initialText,'language': 'en'},headers={'Authorization': '3da836038be5fb570158829ae76d3aeb'})
		print(response.text)

	return t.RenderJson()
	# t = Tropo()
	# #t.startRecording(url = "http://localhost/recording.py")
	# t.ask(choices = "subway, bike, car, autolib", attempts=3, timeout=60, name="color", say = "What transportation system do you prefer? Subway, bike, car or autolib?")	
	# t.on(event = "continue", next ="/continue")
	# return t.RenderJson()
	
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