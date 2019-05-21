import Connextion_cli as Co
import threading
import time
import json

ListeConnected = []
ListeSalon = []

connected = False

name = ""

def parsing(_raw_message):
	x = _raw_message.split(" ", 1)
	if x[0] == "\\t":
		pass
	elif x[0] == "\\c":
		y = x[1].split(" ", 1)
		if y[0] == "+":
			add_ppl(y[1])
		elif y[0] == "-":
			sub_ppl(y[1])
		elif y[0] == "i":
			init_ppl(y[1])
		elif y[0] == "m":
			modif_ppl(y[1])
	elif x[0] == "\\s":
		y = x[1].split(" ", 1)
		if y[0] == "+":
			add_sal(y[1])
		elif y[0] == "-":
			sub_sal(y[1])
		elif y[0] == "0":
			init_sal(y[1])
		elif y[0] == "m":
			modif_sal(y[1])
	elif x[0] == "\\p":
		pass
	elif x[0] == "\\e":
		print("fermetur du serveur")
	elif x[0] == "\\m":
		print (x[1])

################################################## connected gestion   ##################################################

def add_ppl(_nom):									## add a connected
	ListeConnected.append(_nom)
	print("adding " + _nom)

def sub_ppl(_nom):									## delete a connected
	del ListeConnected[ListeConnected.index(_nom)]

def init_ppl(_list_noms):							## init all connected when connect to a serveur
	print("init recup")
	list_noms = _list_noms.split(" ")
	for nom in list_noms:
		add_ppl(nom)

def modif_ppl(_list_noms):							## modifie the name/property(later) of a connected
	list_noms = json.loads(_list_noms)
	ListeConnected[ListeConnected.index(list_noms[0])] = list_noms[1]

def show_conected():								## print all conected
	if ListeConnected == []:
		print("aucun connecter")
	for item in ListeConnected :
		print(item)

#################################################### salon gestion	####################################################

def add_sal(_nom):									## add a salon
	ListeSalon.append(_nom)

def sub_sal(_nom):									## delete a salon
	del ListeSalon[ListeSalon.index(_nom)]

def init_sal(_list_noms):							## init all salon when connect to a serveur
	list_noms = json.loads(_list_noms)
	for nom in list_noms:
		add_sal(nom)

def modif_sal(_list_noms):							## modifie the name/property(later) of a salone
	list_noms = json.loads(_list_noms)
	ListeSalon[ListeSalon.index(list_noms[0])] = list_noms[1]

#################################################### other gestion	####################################################	

def sendName(_txt):									## send the name of the client
	name = _txt
	Co.addBuffer("\\c + " + _txt)


######################## thread witch keep cheking upcomming message in Connexion Reciv Buffer	########################

class myThreadRecup(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global ListeConnected
		while Co.Connextion:
			time.sleep(.05)
			temp = Co.readBuffer()
			if temp != None :
				parsing(temp)


######################################## init and main loop for runnig client	########################################

print ("Enter your name :")
sendName( input())								## waiting the name of the client and send it to te serveur
Co.connect_client()								## lunch procecuse client side serveur

thread = myThreadRecup()						## init thread
thread.start()									## start thread


while Co.Connextion:							## main loop
	txt = input()
	if txt == "e":
		Co.addBuffer("\\e")
		time.sleep(1)
		Co.close_connect()
	if txt == "c":
		show_conected()
	else:
		Co.addBuffer("\\m " + txt)
		