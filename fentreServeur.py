from tkinter import *
import socket
import time
import threading


### patie varialbe "global"
global combo
global entree

global sock
global socketFils

global Discution
global currentConv
global interface


currentConv = []
socketFils = []
Discution = {}

fenetre = Tk()
port = 15555
exitFlag = True
n = 0



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', port ))

def callback():
   global socketFils

   exitFlag = False
   if sock is not None:
      sock.close()
   #TODO close all client.
   for client in socketFils:
      client.close()
   fenetre.destroy()

def verif():
   global Discution
   print (Discution)

def getting (_name): ##gert conv
   global Discution

   return Discution[_name]

def adding(_name): ## add conv 
   global Discution
   Discution[_name] = []

def subbing(_name):## sub conv
   global Discution
   del Discution[_name]

def addLigneConv(_name, txt):
   Discution[_name].append(txt)

def add(_name):
   interface.liste.insert(END, _name)

def sub (_name):
   pass

def onselect(evt):
   w = evt.widget
   index = int(w.curselection()[0])
   value = w.get(index)
   print ('You selected item %d: "%s"' % (index, value))
   interface.affiche(getting(value))



### partie multithreading
# # # thread qui comunique avec le client
class myThreadEcouteClient (threading.Thread):
   def __init__(self, _threadclient, _threadAdress, _nb):
      threading.Thread.__init__(self)
      self.threadclient = _threadclient
      self.threadAdress = _threadAdress
      self.nb = _nb
      print ("{} connected".format(self.threadAdress)) 
      add(format(self.threadAdress))
      adding(format(self.threadAdress))

   def run(self):
        closeFlag = True

        while closeFlag:
            try:
               response = self.threadclient.recv(255)
               if response.decode()[10:] != "":
                  if (response.decode())[10:] == "/stop":
                     closeFlag = False
                     print ("closing " + format(self.threadAdress))
                     self.threadclient.send(str.encode('/stop'))
                  print (response.decode())
                  addLigneConv(format(self.threadAdress), response.decode())
            except Exception as inst :
               print(inst)
               print('erreur, connextion perdu')
               closeFlag = False
        self.threadclient.close()
        print (format(self.threadAdress) + " closed")
        
# # # thread qui boucle pour accepter les conection
class myThreadMainBoucleCO (threading.Thread): 
   def __init__(self):
      threading.Thread.__init__(self)

   def run(self):
      global n
      global exitFlag
      global socketFils

      while exitFlag:
         try:
            sock.listen(5)
            client, address = sock.accept()
            socketFils.append(client)
            newthread = myThreadEcouteClient(client, address, n)
            newthread.start() 
         except Exception as inst :
            print(inst)
            print('erreur, connextion perdu')
            exitFlag = False

      print ("Close")

class Interface(Frame):
   def __init__(self, fenetre, **kwargs):
      fenetre.protocol("WM_DELETE_WINDOW", callback)

      Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
      self.nb_clic = 0
        
      p = PanedWindow(fenetre, orient=HORIZONTAL)
      p.pack(fill=BOTH)
      p.pack()

      # Création de nos widgets
      self.liste = Listbox(p)
      p.add(self.liste)
      self.liste.pack()
      self.liste.bind('<<ListboxSelect>>', onselect)
      p.pack()

      self.message = Label(self, text="Vous n'avez pas cliqué sur le bouton.")
      self.message.pack()
       
      self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
      self.bouton_quitter.pack()
        
      self.bouton_cliquer = Button(self, text="Cliquez ici", fg="red",command=self.cliquer)
      self.bouton_cliquer.pack()


      xscrollbar = Scrollbar(self, orient=HORIZONTAL)
      xscrollbar.pack(side=BOTTOM, fill=X)

      yscrollbar = Scrollbar(self)
      yscrollbar.pack(side=RIGHT, fill=Y)

      self.text = Text(p, wrap=NONE,
                  xscrollcommand=xscrollbar.set,
                  yscrollcommand=yscrollbar.set)
      self.text.pack()
      

      xscrollbar.config(command=self.text.xview)
      yscrollbar.config(command=self.text.yview)
      self.pack()
   
   def affiche(self, Message):
      temp = ""
      for mess in Message:
         temp += mess + "\n"
      self.message["text"] = temp
    
   def cliquer(self):
      #self.nb_clic += 1
      #self.message["text"] = "Vous avez cliqué {} fois.".format(self.nb_clic)
      li = self.liste.get(0,END)
      print(li)
      self.message["text"] = li

# Create new threads
thread1 = myThreadMainBoucleCO()
# Start new Threads
thread1.start()


interface = Interface(fenetre)
interface.mainloop()

print("this is the End folk")