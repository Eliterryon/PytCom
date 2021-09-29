import connexion_cli as Co
import threading
import time
import json
import message


#from interface.fenetreKV import TestApp

ListeConnected = []
ListeSalon = []

App = None

connected = False

name = ""

dicoParse = {}

def parsing(_raw_message):
	x = _raw_message.split(" ", 1)
	if x[0] == "\\t":
		pass
	elif x[0] == "\\c":
		y = x[1].split(" ", 1)
		if y[0] == "+":
			addition_connected(y[1])
		elif y[0] == "-":
			substract_connected(y[1])
		elif y[0] == "i":
			initialisation_connected(y[1])
		elif y[0] == "m":
			modification_connected(y[1])
	elif x[0] == "\\s":
		y = x[1].split(" ", 1)
		if y[0] == "+":
			addition_salon(y[1])
		elif y[0] == "-":
			substract_salon(y[1])
		elif y[0] == "0":
			initialisation_salon(y[1])
		elif y[0] == "m":
			modification_salon(y[1])
	elif x[0] == "\\p":
		pass
	elif x[0] == "\\e":
		print("fermetur du serveur")
	elif x[0] == "\\m":
		y = x[1].split(" ", 1)
		print ("[" + y[0] + "]")
		print ("	" + y[1])
		App.addChat(y[0], y[1])

################################################## connected gestion   ##################################################

def addition_connected(_message):									## add a connected
	ListeConnected.append(_message.message)
	print("adding " + _message.message)

def substract_connected(_message):									## delete a connected
	del ListeConnected[ListeConnected.index(_message.message)]

def initialisation_connected(_message):							## init all connected when connect to a serveur
	print("init recup")
	list_noms = _message.message.split(" ")
	for nom in list_noms:
		addition_connected(nom)

def modification_connected(_message):							## modifie the name/property(later) of a connected
	list_noms = json.loads(_message.message)
	ListeConnected[ListeConnected.index(list_noms[0])] = list_noms[1]

def show_conected():								## print all conected
	if ListeConnected == []:
		print("aucun connecter")
	for item in ListeConnected :
		print(item)

#################################################### salon gestion	####################################################

def addition_salon(_message):									## add a salon
	ListeSalon.append(_message.message)

def substract_salon(_message):									## delete a salon
	del ListeSalon[ListeSalon.index(_message.message)]

def initialisation_salon(_message):							## init all salon when connect to a serveur
	list_noms = json.loads(_message.message)
	for nom in list_noms:
		addition_salon(nom)

def modification_salon(_message):							## modifie the name/property(later) of a salone
	list_noms = json.loads(_message.message)
	ListeSalon[ListeSalon.index(list_noms[0])] = list_noms[1]

####################################################   message gestion	################################################

def new_message(_message):
	print ("[" + _message.author + "]")
	print ("	" + _message.message)
	App.addChat(_message.author, _message.message)

####################################################  other gestion	####################################################	

def sendName(_txt):									## send the name of the client
	name = _txt
	Co.addBuffer("\\c + " + _txt)


#####################################   observeur's method for recovering message	####################################

class ObservReciv():
	def update(_arg):
		try:
			temp = _arg[0]
			if temp != None :
				mess = message.Message(temp)
				dicoParse[mess.mode][mess.submod](mess)
				#parsing(temp)
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
dicoParse[message.MODE.SALON][message.SUB_MODE.ADDITION] = addition_salon
dicoParse[message.MODE.SALON][message.SUB_MODE.SUBSTRACTION] = substract_salon
dicoParse[message.MODE.SALON][message.SUB_MODE.MODIFICATION] = modification_salon
dicoParse[message.MODE.SALON][message.SUB_MODE.INITIALISATION] = initialisation_salon

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


Co.connect_client(ObservReciv)					## lunch procecuse client side serveur
print ("Enter your name :")
sendName( input())								## waiting the name of the client and send it to te serveur
#App = TestApp()
#App.run()


while Co.Connexion:							## main loop
	txt = input()
	if txt == "e":
		Co.addBuffer("\\e")
		time.sleep(3)
		Co.close_connect()
	elif txt == "c":
		show_conected()
	else:
		Co.addBuffer("\\m " + txt)
		