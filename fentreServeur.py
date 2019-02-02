from tkinter import * 
from tkinter import tix
import socket as sockett
import time
import threading


### patie varialbe "global"
global combo
global labelConv
global entree
global socket
global Discution

Discution = {}

fenetre = Tk()
port = 15555
exitFlag = True 
elementListe = ["pierre", "feuille", "ciseau"]
n = 0



socket = sockett.socket(sockett.AF_INET, sockett.SOCK_STREAM)
socket.bind(('', port ))

def callback():
   exitFlag = False
   socket.close()
   #TODO close all client.
   fenetre.destroy()

def Affiche(evt):
   print (varcombo.get())

def adding(_name): ## add conv 
   global Discution
   Discution[_name] = []
   return Discution.get[_name]

def subbing(_name):## sub conv
   global Discution
   del Discution[_name]

def add(_name):
   global n
   combo.insert(n, _name + str(n))   
   n = n + 1

def sub (n):
   combo.subwidget_list['slistbox'].subwidget_list['listbox'].delete(n)
   n = n -1



### partie multithreading
# # # thread qui comunique avec le client
class myThreadEcouteClient (threading.Thread):
   def __init__(self, _threadclient, _threadAdress, _nb):
      threading.Thread.__init__(self)
      self.threadclient = _threadclient
      self.threadAdress = _threadAdress
      self.nb = _nb
      print ("{} connected".format(self.threadAdress)) 
      add(format(self.threadclient))

   def run(self):
        global exitFlag
        closeFlag = True
        while closeFlag:
            response = self.threadclient.recv(255)
            if response != "":
               if (response.decode()) == "/stop":
                  closeFlag = False
                  print ("closing " + format(self.threadAdress))
                  # TODO fermetur connextion client
                  self.threadclient.send(str.encode('/stop'))
               print (response.decode())
        self.threadclient.close()
        print (format(self.threadAdress) + " closed")
        
# # # thread qui boucle pour accepter les conection
class myThreadMainBoucleCO (threading.Thread): 
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
      global n
      global exitFlag
      while exitFlag:
         socket.listen(5)
         client, address = socket.accept()
         newthread = myThreadEcouteClient(client, address, n)
         newthread.start() 
      print ("Close")





fenetre.protocol("WM_DELETE_WINDOW", callback)

p = PanedWindow(fenetre, orient=HORIZONTAL)
p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
p2 = PanedWindow(p, orient=VERTICAL)
p.add(p2)

fenetre.tk.eval('package require Tix')
varcombo = tix.StringVar() 
combo = tix.ComboBox(fenetre, editable=1, dropdown=1, variable=varcombo, command = Affiche)
## TODO select
combo.entry.config(state='readonly')  ## met la zone de texte en lecture seule
p2.add(combo)

labelConv = Label(fenetre, text="Hello World")
labelConv.pack()

value = StringVar() 
value.set("texte par défaut")
entree = Entry(fenetre, textvariable=value, width=30)
entree.pack()


# Create new threads
thread1 = myThreadMainBoucleCO(1, "Thread-1")
# Start new Threads
thread1.start()

fenetre.mainloop()