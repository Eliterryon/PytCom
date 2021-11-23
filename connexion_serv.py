import socket
import threading
import re
import time
import observeur

HOTE = "localhost"
PORT = 15555
SIZE_MESSAGE = r".{1,200}"

BufferRecive = []  ## buffer for recived message : [ID][msg]

ObserverRecive = observeur.Observer()

ListeClient = {}  ## liste of client : ListeClient[id] = [socket, is_connected]

Connexion = True
socks = None


################################################ thread serveur side	###############################################


class myThreadRevived(
    threading.Thread
):  ## thraed who wait a upcomming message (1 for each client)
    def __init__(self, _sock, _id):
        threading.Thread.__init__(self)
        self.sock = _sock
        self.id = _id

    def run(self):
        global ListeClient
        global BufferRecive
        global ObserverRecive

        while (self.id in ListeClient) and ListeClient[self.id][1]:
            try:
                temp = custom_recive(self.sock.recv(255), self.sock)
            except socket.timeout:
                pass
            except Exception as err:
                if (self.id in ListeClient) and ListeClient[self.id][1]:
                    close_connect(self.id, True)
                    print(err)
                    print("connexion lose (" + format(self.id) + ") (Erreur 4)")
                elif (self.id in ListeClient) and ListeClient[self.id][1] == False:
                    print(format(self.id) + " diconected")
                    close_connect(self.id, True)
                else:
                    print("connexion " + format(self.id) + " closed")
            else:
                BufferRecive.append((self.id, temp))
                ObserverRecive.notify(readBuffer())


class myThreadServ(threading.Thread):  ## thread that manage new upcomming connexion
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global ListeClient
        global Connexion
        global socks

        while Connexion:
            try:
                socks.listen(5)
                sockc, id = socks.accept()
            except socket.timeout:
                pass
            except Exception as err:
                if Connexion:
                    print(err)
                    print("erreur, connexion perdu (Erreur 3)")
                    Connexion = False
                else:
                    Connexion = False
                    print("serveur socket closed")
            else:
                sockc.settimeout(2)
                ListeClient[format(id)] = [sockc, True]
                lunchClient(sockc, format(id))


################################################### message gestion	###################################################


def custom_send(_message, _sockc):  ## cut and send leaving msg to designated socket
    liste = re.findall(SIZE_MESSAGE, _message)
    temp = liste.pop()
    for i in liste:
        _sockc.send(str.encode(i + "\suit"))
    _sockc.send(str.encode(temp + "\stop"))


def custom_recive(
    _message, _sockc
):  ## recive and concaten upcomming msg from designated socket
    message = _message.decode()
    if re.match(r"(.)*(\\suit)$", message) is not None:
        temp = message[:-5] + custom_recive(_sockc.recv(255))
        return temp
    elif re.match(r"(.)*(\\stop)$", message) is not None:
        temp = message[:-5]
        return temp


############################################# serveux connexion gestion	############################################


def lunchClient(_sock, _id):  ## lunch a new connected client
    threadR = myThreadRevived(_sock, _id)
    threadR.name = "ClientThreadRevived"
    threadR.start()
    print("client " + format(_id) + "is connected")


def stop():  ## stop the serveur
    global Connexion
    global ListeClient
    global socks

    Connexion = False
    for id in ListeClient.keys():
        close_connect(id, False)
    ListeClient = {}
    socks.close()
    time.sleep(0.01)
    print("serveur closed")


def connect_serveur(
    ObserverReciveFonction, _hote=HOTE, _port=PORT
):  ## open port and lunchClient thread for connection serveur side
    global socks
    global ObserverRecive

    try:
        socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socks.bind(("", _port))
        socks.settimeout(2)
        thread = myThreadServ()
        thread.name = "ThreadServ"
        thread.start()
        print("connected")

        ObserverRecive.attach(ObserverReciveFonction)

        return True

    except Exception as err:
        print(err)
        print("error, can't opend serveur port (Erreur 1)")
        return False


def close_connect(
    _id_client, booll
):  ## close the connection of a _id_client if booll it is bc we los the connection
    global ListeClient
    ListeClient[_id_client][1] = False
    ListeClient[_id_client][0].close()
    if booll:
        del ListeClient[_id_client]


def deco_client(_id_client):  ## take in count that the client disconnect
    global ListeClient
    ListeClient[_id_client][1] = False


#################################################### Buffer gestion	###################################################


def addBuffer(_id, _msg):  ## add a msg to the bufferSend for sending it
    if ListeClient[_id][1]:
        custom_send(_msg, ListeClient[_id][0])


def readBuffer():  ## return the 1st msg to the BufferRecive, return None if empty
    global BufferRecive
    if len(BufferRecive) > 0:
        temp = BufferRecive[0]
        del BufferRecive[0]
        return temp
    else:
        return None
