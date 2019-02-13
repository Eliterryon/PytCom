# coding: utf-8
from tkinter import *
import socket as sockett
import threading
import sys
from time import gmtime,strftime
import fenetre as FEN

hote = "localhost"
port = 15555

STAT_CONNEXTION = False
socket = None

Name = ""
fenetre = Tk()

def close_client():
    global STAT_CONNEXTION
    global Run

    if STAT_CONNEXTION :
        close_connextion(False)

    Run = False

def close_connextion(_by_serv):
    global STAT_CONNEXTION
    if (_by_serv):
        print("connextion closed by serveur")
    else:
        send_message("connextion closed by client")
        print("connextion closed by client")
    STAT_CONNEXTION = False

def connect_socket(hote=hote, port=port) :
    global STAT_CONNEXTION
    global socket

    try:
        socket = sockett.socket(sockett.AF_INET, sockett.SOCK_STREAM)
        socket.setsockopt(sockett.SOL_SOCKET, sockett.SO_REUSEADDR, 1)
        socket.connect((hote, port))
        STAT_CONNEXTION = True
        print ("Connection on {}".format(port))

        # Create new threads
        threadR = myThreadRevived(socket)
        # Start new Threads
        threadR.start()
        return True

    except Exception as inst :
        print(inst)
        socket.close()
        print ("erreur, Connexion immpossible (Erreur 3)")
        return False

def loop_connection():
    global STAT_CONNEXTION

    while STAT_CONNEXTION:
        inp = input()
        if inp == "/close":
            close_client()
        if inp == "/stop":
            close_connextion(False)
        else:
            send_message(inp)

def button_envoyer():
   pass
   #send_message(interface.saisi.get())
   

def send_message(inp):
    global STAT_CONNEXTION
    
    snd = (strftime("%H.%M.%S", gmtime()) + ": " + inp)
    try:
        socket.send(str.encode(snd))
    except Exception as err :
        print(err)
        print("erreur, Connexion disparue (Erreur 2)")

##Tread recive##
class myThreadRevived (threading.Thread):
    def __init__(self, thread):
        threading.Thread.__init__(self)
        self.daemon = True
        self.thread = thread
    def run(self):
        global STAT_CONNEXTION

        while STAT_CONNEXTION:
            try:
                response = self.thread.recv(255)
            except Exception as err :
                print(err)
                print("erreur de connextion (Erreur 1)")
                close_connextion(True)
                print(STAT_CONNEXTION)
            if (response.decode())[10:] == "/stop":
                close_connextion(True)
            print(response.decode())


Run = True
print("client runnig")
while Run:
    inp = input()
    if inp == "/close":
        close_client()
    elif inp == "/connect":
        if connect_socket():
            loop_connection()
    else:
        print("cmd inconnue")

"""
try:
   interface = FEN.Interface(fenetre)
   #interface.liste.bind('<<ListboxSelect>>', onselect)
   interface.valider.configure(command=send_message)
   interface.mainloop()
except Exception as inst :
   print(inst)
   #TODO

"""