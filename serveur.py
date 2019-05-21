import Connextion_serv as Co
import threading
import time
import json

ListeConnected = {} 								## liste of connectesd :[id] = nom
ListeSalon = []										## liste of connectesd


def parsing(_id, _raw_message):
	x = _raw_message.split(" ", 1)
	if x[0] == "\\t":
		pass
	elif x[0] == "\\c":
		y = x[1].split(" ", 2)
		if y[0] == "+":
			add_ppl(y[1], _id)
		elif y[0] == "-":
			sub_ppl(y[1],_id)
		elif y[0] == "m":
			modif_ppl(y[1], _id)
	elif x[0] == "\\s":
		pass
	elif x[0] == "\\p":
		pass
	elif x[0] == "\\e":
		Co.deco_client(_id)
	elif x[0] == "\\m":
		msg_all(_raw_message, _id)
		print (x[1])

################################################## connected gestion   ##################################################

def add_ppl(_nom, _id):								## add a connected
	msg_all("\\c + " + _nom)
	if len(ListeConnected) > 0 :
		temp = ""
		for values in ListeConnected.values():
			temp += values + " "
		print(temp)
		Co.addBuffer(_id,"\\c i " + temp[:-1])
	ListeConnected[_id] = _nom

def sub_ppl(_nom, _id):								## delete a connected 
	Co.close_connect(_id, True)
	del ListeConnected[_id]
	msg_all("\\c - " + _nom)

def modif_ppl(_new_name, _id):						## modifie the name/property(later) of a connected
	msg_all("\\c m " + json.dumps([ListeConnected[_id], _new_name]), _id)
	ListeConnected[_id] = _new_name

def msg_all(_msg, avoid = None):					## send a message to all connected
	for key in ListeConnected.keys() :
		if key != avoid :
			Co.addBuffer(key, _msg)

def show_conected():								## print all conected
	if Co.ListeClient == {}:
		print("aucun connecter")
	for key, item in Co.ListeClient.items() :
		print(ListeConnected[key], item[1])

######################### thread witch keep cheking upcomming message in Connexion Reciv Buffer	#########################

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

######################################## init and main loop for runnig client	########################################

Co.connect_serveur()								## lunch procecuse serveur side serveur
thread = myThreadRecup()							## init thread
thread.start()										## lunch thread


while Co.Connextion:								## main loop
	txt = input()
	if txt == "e":
		msg_all("\\e")
		time.sleep(1)
		Co.stop()
		time.sleep(1)
	if txt == "c":
		show_conected()
	else:
		msg_all("\\m " + txt)
