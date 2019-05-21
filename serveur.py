import Connextion_serv as Co
import threading
<<<<<<< HEAD
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
=======
import fenetre as FEN
from time import gmtime,strftime


### patie varialbe "global"
global combo
global entree

global sock
global socketFils


global Discution
global currentConv
global interface


currentConv = []
socketFils = {}
currentsocket = None
Discution = {}
currentDiscution = ""

fenetre = Tk()

port = 15555
exitFlag = True
n = 0



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', port ))

def callback():
   global socketFils
   
   if sock is not None:
      sock.close()
   for client in socketFils:
      if socketFils[client] != None:
         deco(socketFils[client], client, True)
   fenetre.destroy()


def deco(_sock, _name, _by_serv):
   global socketFils

   print ("closing " + format(_name))
   
   if _by_serv :
      envoie("serveur shutdown", _sock)

   _sock.close()
   socketFils[_name]=None

def getting (_name): ##gert conv
   global Discution

   return Discution[_name]

def adding(_name, _sock): ## add conv 
   global socketFils
   global Discution
   
   interface.add(_name) 
   Discution[_name] = []
   socketFils[_name]=_sock

def subbing(_name):## sub conv
   global Discution
   del Discution[_name]

def addLigneConv(_name, txt):
   if currentDiscution == _name:
      interface.addaffiche(txt)
   Discution[_name].append(txt)

def onselect(evt):
   global currentDiscution
   global currentsocket
   global socketFils

   interface.clean() 
   w = evt.widget 
   index = int(w.curselection()[0])
   value = w.get(index)

   currentDiscution = value
   currentsocket = socketFils[value]

   print (currentsocket)
   interface.affiche(getting(value))

def envoie(_inp, _sock):
   if _sock != None or _sock != "" :
      snd = (strftime("%H.%M.%S", gmtime()) + ": " + _inp)
      try:
         _sock.send(str.encode(snd))
         addLigneConv(format(_sock), snd) ### TODO plante la
      except Exception as err :
         print(err)
         print("erreur, Connexion disparue (Erreur 1)")
   else:
      print("erreur, aucune connexion selectioner (Erreur 4)")

def envoyer():
   global currentsocket

   try:
      envoie(interface.saisi.get(), currentsocket)
      interface.saisi.delete(0, END)
   except Exception as err :
      print(err)

### partie multithreading
# # # thread qui comunique avec le client
class myThreadEcouteClient (threading.Thread):
   def __init__(self, _threadclient, _threadAdress, _nb):
      threading.Thread.__init__(self)
      self.threadclient = _threadclient
      self.threadAdress = _threadAdress
      self.nb = _nb
      print ("{} connected".format(self.threadAdress))
      adding(format(self.threadAdress), self.threadclient)
      

   def run(self):
        closeFlag = True

        while closeFlag:
            try:
               response = self.threadclient.recv(255)

               if response.decode()[10:] != "":
                  if (response.decode())[10:] == "connextion closed by client":
                     closeFlag = False
                     deco(self.threadclient, self.threadAdress, False)
                  else:
                     print (response.decode())
                     addLigneConv(format(self.threadAdress), response.decode())

            except Exception as inst :
               print(inst)
               print('erreur, connextion perdu (Erreur 2)')
               closeFlag = False
               deco(self.threadclient, self.threadAdress, False)

        print (format(self.threadAdress) + " closed")
        
# # # thread qui boucle pour accepter les conection
class myThreadMainBoucleCO (threading.Thread): 
   def __init__(self):
      threading.Thread.__init__(self)

   def run(self):
      global n
      global socketFils

      exitFlag = True
      while exitFlag:
         try:
            sock.listen(5)
            client, address = sock.accept()
            newthread = myThreadEcouteClient(client, address, n)
            newthread.start() 
         except Exception as inst :
            print(inst)
            print('erreur, connextion perdu (Erreur 3)')
            exitFlag = False

      print ("Close")

# Create new threads
thread1 = myThreadMainBoucleCO()
# Start new Threads
thread1.start()

try:
   interface = FEN.Interface(fenetre)
   interface.liste.bind('<<ListboxSelect>>', onselect)
   interface.valider.configure(command=envoyer)
   interface.mainloop()
except Exception as err :
   print(err)

callback()
print("this is the End folk")
>>>>>>> master
