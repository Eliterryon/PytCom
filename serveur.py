from tkinter import *
import socket
import time
import threading
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
   #TODO close all client.
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

   print ('You selected item %d: "%s"' % (index, value))
   interface.affiche(getting(value))

def envoie(_inp, _sock):
   global currentsocket

   snd = (strftime("%H.%M.%S", gmtime()) + ": " + _inp)
   try:
      _sock.send(str.encode(snd))
      addLigneConv(_sock, snd)

   except:
      print("erreur, Connexion disparue (Erreur 1)")

def envoyer():
   try:
      envoie(interface.saisi.get(), currentDiscution)
      interface.saisi.delete(0, END)
   except:
      pass

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
except Exception as inst :
   print(inst)

callback()
print("this is the End folk")