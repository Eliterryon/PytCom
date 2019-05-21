import Connextion_serv as Co
import threading
import time
import json

ListeConnected = {} # 
ListeSalon = []

def parsing(_id, _raw_message):
	x = _raw_message.split(" ", 1)
	if x[0] == "\\t":
		pass
	elif x[0] == "\\c":
		y = x[1].split(" ", 2)
		if y[0] == "+":
			addppl(y[1], _id)
		elif y[0] == "-":
			subppl(y[1],_id)
		elif y[0] == "m":
			modifppl(y[1], _id)
	elif x[0] == "\\s":
		pass
	elif x[0] == "\\p":
		pass

def addppl(_nom, _id):
	msg_all("\\c + " + _nom)
	if len(ListeConnected) > 0 :
		temp = ""
		for values in ListeConnected.values():
			temp += " " + values
		print(temp)
		Co.addBuffer(_id,"\\c i " + temp)
	ListeConnected[_id] = _nom
def subppl(_nom, _id):
	del ListeConnected[_id]
	msg_all("\\c - " + _nom)
def modifppl(_new_name, _id):
	msg_all("\\c m " + json.dumps([ListeConnected[_id], _new_name]), _id)
	ListeConnected[_id] = _new_name

def msg_all(_msg, avoid = None):
	for key in ListeConnected.keys() :
		if key != avoid :
			Co.addBuffer(key, _msg)





class myThreadRecup(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global ListeConnected
		while Co.Connextion:
			time.sleep(.05)
			temp = Co.readBuffer()
			if temp != None :
				parsing(temp[0], temp[1])
				#print(ListeConnected)



Co.connect_serveur()
thread = myThreadRecup()
thread.start()


while Co.Connextion:
	txt = input()
	if txt == "e":
		Co.stop()
		time.sleep(1)
	else:
		msg_all(txt)
