# coding: utf-8

import socket as sockett
import threading
import sys
from time import gmtime,strftime

hote = "localhost"
port = 15555

CON = False
socket = None

def stop():
    global CON
    global socket

    if socket is not None:
        socket.close()
    print("Close")
    CON = False

def connect(hote=hote, port=port) :
    global CON
    global socket

    try:
        socket = sockett.socket(sockett.AF_INET, sockett.SOCK_STREAM)
        socket.setsockopt(sockett.SOL_SOCKET, sockett.SO_REUSEADDR, 1)
        socket.connect((hote, port))
        CON = True
        print ("Connection on {}".format(port))

        # Create new threads
        threadR = myThreadRevived(socket)
        # Start new Threads
        threadR.start()

    except:
        socket.close()
        print ('erreur, Connexion immpossible')

##Tread recive##
class myThreadRevived (threading.Thread):
    def __init__(self, thread):
        threading.Thread.__init__(self)
        self.daemon = True
        self.thread = thread
    def run(self):
        global CON

        while CON:
            try:
                response = self.thread.recv(255)
            except:
                print("erreur, Connexion disparue")
                stop()
            if (response.decode()) == "/stop":
                print (" Connexion Fermée")
                stop()
            print(response.decode())

def send(inp):
    global CON
    
    snd = (strftime("%H.%M.%S", gmtime()) + ": " + inp)
    try:
        socket.send(str.encode(snd))
    except:
        print("erreur, Connexion disparue")
        stop()

def close():
    global CON
    global Run

    if CON == True:
        send("/stop")
    CON = False
    Run = False

def loop_connection():
    global CON

    while CON:
        inp = input()
        if inp == "/close":
            close()
        if inp == "/stop":
            CON = False
            send("/stop")
        else:
            send(inp)
Run = True
while Run:
    try:
        inp = input()
    except (KeyboardInterrupt, SystemExit):
        raise

    if inp == "/close":
        close()
        Run = False
    elif inp == "/connect":
        connect()
        if CON:
            loop_connection()
    else:
        print("cmd inconnue")