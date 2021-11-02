import connexion_serv as Co
import threading
import time
import json
import message


ListeConnected = {} 								## liste of connectesd :[id] = nom
ListeSalon = []										## liste of connectesd

dicoParse = {}

def parsing(_id, _raw_message):
	x = _raw_message.split(" ", 1)
	if x[0] == "\\t":
		pass
	elif x[0] == "\\c":
		y = x[1].split(" ", 2)
		if y[0] == "+":
			addition_connected(y[1], _id)						## TODO name without space
		elif y[0] == "-":
			substract_connected(y[1],_id)
		elif y[0] == "m":
			modification_connected(y[1], _id)
	elif x[0] == "\\s":
		pass
	elif x[0] == "\\p":
		pass
	elif x[0] == "\\e":
		substract_connected(ListeConnected[_id], _id)
	elif x[0] == "\\m":
		new_message("\\m " + ListeConnected[_id] + " " + x[1], _id)
		print ("[" + ListeConnected[_id] + "]")
		print ("	" + x[1])

##################################################  connected gestion	##################################################

def addition_connected(_message, _id):								## add a connected
	new_message(_message)
	
	ListeConnected[_id] = _message.message

def substract_connected(_message, _id):								## delete a connected 
	Co.deco_client(_id)
	time.sleep(0.5)
	print(_message.message," c'est deconecter")
	new_message(_message)

def modification_connected(_message, _id):							## modifie the name/property(later) of a connected
	new_message(_message, _id)
	ListeConnected[_id] = _message.message

def initialisation_connected(_message, _id):
	if len(ListeConnected) > 0 :
		temp = ""
		for values in ListeConnected.values():
			temp += values + " "
		print(temp)
		Co.addBuffer(_id,"\\c i " + temp[:-1])

def show_conected():												## print all conected
	if Co.ListeClient == {}:
		print("aucun connecter")
	for key, item in Co.ListeClient.items() :
		print(ListeConnected[key], item[1])

##################################################  connected gestion	##################################################

def new_message(_message, _id = None):									## send a message to all connected
	for key in ListeConnected.keys() :
		if key != _id :
			Co.addBuffer(key, _message.message)

######################### thread witch keep cheking upcomming message in Connexion Reciv Buffer	#########################

class ObservReciv():
	def update(_arg):
		try:
			temp = _arg[0]
			if temp != None and temp[1] != None:
				mess = message.Message(temp[0])
				dicoParse[mess.mode][mess.submod](mess,temp[1])
		except:
			pass

###########################################   Neasted parsing dictionairy	############################################


dicoParse[message.MODE.MESSAGE]= {}
dicoParse[message.MODE.MESSAGE][message.SUB_MODE.NULL] = new_message

dicoParse[message.MODE.CLOSING]= {}
dicoParse[message.MODE.CLOSING][message.SUB_MODE.NULL] = Co.close_connect

dicoParse[message.MODE.PRIVAT_MESSAGE]= {}
dicoParse[message.MODE.PRIVAT_MESSAGE][message.SUB_MODE.NULL] = Co.close_connect

dicoParse[message.MODE.SALON]= {}
#dicoParse[message.MODE.SALON][message.SUB_MODE.ADDITION] = addition_salon
#dicoParse[message.MODE.SALON][message.SUB_MODE.SUBSTRACTION] = substract_salon
#dicoParse[message.MODE.SALON][message.SUB_MODE.MODIFICATION] = modification_salon
#dicoParse[message.MODE.SALON][message.SUB_MODE.INITIALISATION] = initialisation_salon

dicoParse[message.MODE.SETTING]= {}
dicoParse[message.MODE.SETTING][message.SUB_MODE.ADDITION] = Co.close_connect
dicoParse[message.MODE.SETTING][message.SUB_MODE.SUBSTRACTION] = Co.close_connect
dicoParse[message.MODE.SETTING][message.SUB_MODE.MODIFICATION] = Co.close_connect
dicoParse[message.MODE.SETTING][message.SUB_MODE.INITIALISATION] = Co.close_connect

dicoParse[message.MODE.CONNECTION]= {}
dicoParse[message.MODE.CONNECTION][message.SUB_MODE.ADDITION] = addition_connected
dicoParse[message.MODE.CONNECTION][message.SUB_MODE.SUBSTRACTION] = substract_connected
dicoParse[message.MODE.CONNECTION][message.SUB_MODE.MODIFICATION] = modification_connected
dicoParse[message.MODE.CONNECTION][message.SUB_MODE.INITIALISATION] = initialisation_connected

######################################## init and main loop for runnig client	########################################

Co.connect_serveur(ObservReciv)										## lunch procecuse serveur side serveur

while Co.Connexion:													## main loop
	txt = input()
	if txt == "e":

		new_message("\\e")
		time.sleep(1)
		Co.stop()
		time.sleep(1)
		exit()
	elif txt == "c":
		show_conected()
	else:
		mm = message.Message(message.MODE.MESSAGE,"serveur", txt, message.SUB_MODE.NULL,)
		new_message(mm)
