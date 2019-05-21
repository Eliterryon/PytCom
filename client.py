import Connextion_cli as Co
import threading
import time
import json

ListeConnected = []
ListeSalon = []

connected = False

def parsing(_raw_message):
	x = _raw_message.split(" ", 1)
	if x[0] == "\\t":
		pass
	elif x[0] == "\\c":
		y = x[1].split(" ", 1)
		if y[0] == "+":
			addppl(y[1])
		elif y[0] == "-":
			subppl(y[1])
		elif y[0] == "i":
			initppl(y[1])
		elif y[0] == "m":
			modifppl(y[1])
	elif x[0] == "\\s":
		y = x[1].split(" ", 1)
		if y[0] == "+":
			addsal(y[1])
		elif y[0] == "-":
			subsal(y[1])
		elif y[0] == "0":
			initsal(y[1])
		elif y[0] == "m":
			modifsal(y[1])
	elif x[0] == "\\p":
		pass
	else:
		print(_raw_message)

def addppl(_nom):
	ListeConnected.append(_nom)
	print("adding " + _nom)
def subppl(_nom):
	del ListeConnected[ListeConnected.index(_nom)]
def initppl(_list_noms):
	list_noms = _list_noms.split(" ")
	for nom in list_noms:
		addppl(nom)
def modifppl(_list_noms):
	list_noms = json.loads(_list_noms)
	ListeConnected[ListeConnected.index(list_noms[0])] = list_noms[1]

def addsal(_nom):
	ListeSalon.append(_nom)
def subsal(_nom):
	del ListeSalon[ListeSalon.index(_nom)]
def initsal(_list_noms):
	list_noms = json.loads(_list_noms)
	for nom in list_noms:
		addsal(nom)
def modifsal(_list_noms):
	list_noms = json.loads(_list_noms)
	ListeSalon[ListeSalon.index(list_noms[0])] = list_noms[1]

def sendName(_txt):
	Co.addBuffer("\\c + " + _txt)




class myThreadRecup(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		print("init recup")
		global ListeConnected
		while Co.Connextion:
			time.sleep(.05)
			temp = Co.readBuffer()
			if temp != None :
				print("recup")
				parsing(temp)





sendName( input())
Co.connect_client()

thread = myThreadRecup()
thread.start()


while Co.Connextion:
	txt = input()
	if txt == "e":
		Co.close_connect()
	else:
		Co.addBuffer(txt)
		