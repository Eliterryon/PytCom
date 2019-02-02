# coding: utf-8

import socket as sockett
import threading
import sys

hote = "localhost"
port = 15555

global Run
global Con
Con = False
Run = True
global socket

def Exit():
    socket.close()
    print ("Close")
    sys.exit()

def connect(host, por) :
    global Con
    global socket
    try:
        socket = sockett.socket(sockett.AF_INET, sockett.SOCK_STREAM)
        socket.setsockopt(sockett.SOL_SOCKET, sockett.SO_REUSEADDR, 1)
        socket.connect((hote, por))
        Con = True
        print ("Connection on {}".format(port))

        # Create new threads
        threadR = myThreadRevived(socket)
        # Start new Threads
        threadR.start()

    except:
        print ('erreur, Connextion immpossible')
        Exit()


##Tread recive## 
class myThreadRevived (threading.Thread): 
    def __init__(self, thread):
        threading.Thread.__init__(self)
        self.thread = thread
    def run(self):
        response = self.thread.recv(255)
        if (response.decode()) == "/stop":
            global Con 
            Con = False
            print (' Connextion Fermer')
            Exit()
        print(response.decode())

while Run:
    imp = input()
    if Con == False :
        if imp == "/connect":
            connect(hote, port)
        else :
            if imp == "/close":
                Run = False
                print("fermeture")
            else :
                print ("cmd inconu")
    if Con == True:
        if imp == "/close":
            Run = False
            print("fermeture")
            imp = "/stop"
        try:
            socket.send(str.encode(imp))
        except:
            print ('erreur, Connextion disparu')
            Run = False 
