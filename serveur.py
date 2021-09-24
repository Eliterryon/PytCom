import connexion_serv as Co
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
			add_ppl(y[1], _id)						## TODO name without space
		elif y[0] == "-":
			sub_ppl(y[1],_id)
		elif y[0] == "m":
			modif_ppl(y[1], _id)
	elif x[0] == "\\s":
		pass
	elif x[0] == "\\p":
		pass
	elif x[0] == "\\e":
		sub_ppl(ListeConnected[_id], _id)
	elif x[0] == "\\m":
		msg_all("\\m " + ListeConnected[_id] + " " + x[1], _id)
		print ("[" + ListeConnected[_id] + "]")
		print ("	" + x[1])

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
	Co.deco_client(_id)
	time.sleep(0.5)
	print(_nom," c'est deconecter")
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

class ObservReciv():
	def update(arg):
		try:
			temp = arg[0]
			if temp != None and temp[1] != None:
				parsing(temp[0], temp[1])
		except:
			pass

######################################## init and main loop for runnig client	########################################

Co.connect_serveur(ObservReciv)						## lunch procecuse serveur side serveur

while Co.Connexion:								## main loop
	txt = input()
	if txt == "e":
		msg_all("\\e")
		time.sleep(1)
		Co.stop()
		time.sleep(1)
		exit()
	elif txt == "c":
		show_conected()
	else:
		msg_all("\\m serveur " + txt)
