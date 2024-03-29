import connexion_cli as Co
import threading
import time
import json
import message


# from interface.fenetreKV import TestApp

ListeConnected = []
ListeSalon = []

App = None

connected = False

name = ""

dicoParse = {}

################################################## connected gestion   ##################################################


def addition_connected(_message):  ## add a connected
    ListeConnected.append(_message.message)
    print("adding " + _message.message)


def substract_connected(_message):  ## delete a connected
    del ListeConnected[ListeConnected.index(_message.message)]


def initialisation_connected(_message):  ## init all connected when connect to a serveur
    print("init recup")
    list_noms = _message.message.split(" ")
    for nom in list_noms:
        addition_connected(nom)


def modification_connected(
    _message
):  ## modifie the name/property(later) of a connected
    list_noms = json.loads(_message.message)
    ListeConnected[ListeConnected.index(list_noms[0])] = list_noms[1]


def show_conected():  ## print all conected
    if ListeConnected == []:
        print("aucun connecter")
    for item in ListeConnected:
        print(item)


#################################################### salon gestion	####################################################


def addition_salon(_message):  ## add a salon
    ListeSalon.append(_message.message)


def substract_salon(_message):  ## delete a salon
    del ListeSalon[ListeSalon.index(_message.message)]


def initialisation_salon(_message):  ## init all salon when connect to a serveur
    list_noms = json.loads(_message.message)
    for nom in list_noms:
        addition_salon(nom)


def modification_salon(_message):  ## modifie the name/property(later) of a salone
    list_noms = json.loads(_message.message)
    ListeSalon[ListeSalon.index(list_noms[0])] = list_noms[1]


####################################################   message gestion	################################################


def new_message(_message):
    print("[" + _message.author + "]")
    print("	" + _message.message)
    App.addChat(_message.author, _message.message)


####################################################  other gestion	####################################################


def sendName(_txt):  ## send the name of the client
    name = _txt
    mess = message.Message(
        _mode=message.MODE.CONNECTION,
        _author=name,
        _message=name,
        _submod=message.SUB_MODE.ADDITION,
    )
    Co.addBuffer(mess)


#####################################   observeur's method for recovering message	####################################


class ObservReciv:
    def update(_arg):
        try:
            temp = _arg[0]
            if temp != None:
                mess = message.Message(_raw_message=temp)
                dicoParse[mess.mode][mess.submod](mess)
        except:
            pass


###########################################   Neasted parsing dictionairy	############################################


dicoParse[message.MODE.MESSAGE] = {}
dicoParse[message.MODE.MESSAGE][message.SUB_MODE.NULL] = new_message

dicoParse[message.MODE.CLOSING] = {}
dicoParse[message.MODE.CLOSING][message.SUB_MODE.NULL] = Co.close_connect

dicoParse[message.MODE.PRIVAT_MESSAGE] = {}
dicoParse[message.MODE.PRIVAT_MESSAGE][message.SUB_MODE.NULL] = Co.close_connect

dicoParse[message.MODE.SALON] = {}
dicoParse[message.MODE.SALON][message.SUB_MODE.ADDITION] = addition_salon
dicoParse[message.MODE.SALON][message.SUB_MODE.SUBSTRACTION] = substract_salon
dicoParse[message.MODE.SALON][message.SUB_MODE.MODIFICATION] = modification_salon
dicoParse[message.MODE.SALON][message.SUB_MODE.INITIALISATION] = initialisation_salon

dicoParse[message.MODE.SETTING] = {}
dicoParse[message.MODE.SETTING][message.SUB_MODE.ADDITION] = Co.close_connect
dicoParse[message.MODE.SETTING][message.SUB_MODE.SUBSTRACTION] = Co.close_connect
dicoParse[message.MODE.SETTING][message.SUB_MODE.MODIFICATION] = Co.close_connect
dicoParse[message.MODE.SETTING][message.SUB_MODE.INITIALISATION] = Co.close_connect

dicoParse[message.MODE.CONNECTION] = {}
dicoParse[message.MODE.CONNECTION][message.SUB_MODE.ADDITION] = addition_connected
dicoParse[message.MODE.CONNECTION][message.SUB_MODE.SUBSTRACTION] = substract_connected
dicoParse[message.MODE.CONNECTION][
    message.SUB_MODE.MODIFICATION
] = modification_connected
dicoParse[message.MODE.CONNECTION][
    message.SUB_MODE.INITIALISATION
] = initialisation_connected


######################################## init and main loop for runnig client	########################################


Co.connect_client(ObservReciv)  ## lunch procecuse client side serveur
print("Enter your name :")
name = input()
sendName(name)  ## waiting the name of the client and send it to te serveur
# App = TestApp()
# App.run()


while Co.Connexion:  ## main loop
    txt = input()
    if txt == "e":
        mm = message.Message(
            _mode=message.MODE.CLOSING,
            _author="serveur",
            _message=txt,
            _submod=message.SUB_MODE.NULL,
        )
        Co.addBuffer(mm)
        time.sleep(3)
        Co.close_connect()
    elif txt == "c":
        show_conected()
    else:
        mm = message.Message(
            _mode=message.MODE.MESSAGE,
            _author=name,
            _message=txt,
            _submod=message.SUB_MODE.NULL,
        )
        Co.addBuffer(mm)
