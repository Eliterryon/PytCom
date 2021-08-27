import socket
import threading
import re
import time
import Observeur 

HOTE = "localhost"
PORT = 15555

BufferRecive = []									## buffer for recived message : [ID][msg]

ObserverRecive = Observeur.Observer()

ListeClient = {}									## liste of client : ListeClient[id] = [socket, is_connected]

Connextion = True									
socks = None



################################################ thread serveur side	###############################################

class myThreadRevived (threading.Thread):			## thraed who wait a upcomming message (1 for each client)
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
				temp = myrecive(self.sock.recv(255), self.sock)
				BufferRecive.append( (self.id, temp) )
				ObserverRecive.notify()

			except Exception as err :
				if (self.id in ListeClient) and ListeClient[self.id][1] :
					close_connect(self.id,True)
					print(err)
					print('connextion lose (' + format(self.id) + ') (Erreur 4)')
				elif (self.id in ListeClient) and ListeClient[self.id][1] == False :
					print(format(self.id) + ' diconected')
					close_connect(self.id,True)
				else:
					print('connextion ' + format(self.id) + ' closed')

class myThreadServ (threading.Thread): 				## thread that manage new upcomming connextion
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global ListeClient
		global Connextion
		global socks
		socks.settimeout(2)

		while Connextion:
			try:				
				socks.listen(5)
				sockc, id = socks.accept()
				ListeClient[format(id)] = [sockc, True]
				lunchClient(sockc,format(id))
			except socket.timeout:
				pass
			except Exception as err :
				if Connextion :
					print(err)
					print('erreur, connextion perdu (Erreur 3)')
					Connextion = False
				else:
					Connextion = False
					print('serveur socket closed')

################################################### message gestion	###################################################

def my_send(_message, _sockc):						## cut and send leaving msg to designated socket
	liste = re.findall(r".{1,200}", _message)
	temp = liste.pop()
	for i in liste :
		_sockc.send(str.encode(i+"\suit"))
	_sockc.send(str.encode(temp+"\stop"))

def myrecive(_message, _sockc):						## recive and concaten upcomming msg from designated socket
	message = _message.decode()
	if re.match(r"(.)*(\\suit)$", message) is not None :
		temp = message[:-5] + myrecive(_sockc.recv(255))
		return (temp)
	elif re.match(r"(.)*(\\stop)$", message) is not None :
		temp = message[:-5]
		return (temp)

############################################# serveux connextion gestion	############################################

def lunchClient(_sock, _id):								## lunch a new connected client
	threadR = myThreadRevived(_sock, _id)
	threadR.name = 'ClientThreadRevived'
	threadR.start()
	print("client " + format(_id) + "is connected")

def stop():									## stop the serveur 
	global Connextion
	global ListeClient
	global socks

	Connextion = False
	for id in ListeClient.keys():
		close_connect(id, False)
	ListeClient = {}
	socks.close()
	time.sleep(0.01)
	print("serveur closed")

def connect_serveur(ObserverReciveFonction, _hote=HOTE, _port=PORT) :		## open port and lunchClient thread for connection serveur side
	global socks
	global ObserverRecive

	try:
		socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socks.bind(('', _port ))
		thread = myThreadServ()
		thread.name = "ThreadServ"
		thread.start()
		print("connected")

		ObserverRecive.attach(ObserverReciveFonction)

		return True

	except Exception as err :
		print(err)
		print("error, can\'t opend serveur port (Erreur 1)")
		return False
	
def close_connect(_id_client, booll):				## close the connection of a _id_client if booll it is bc we los the connection
	global ListeClient
	ListeClient[_id_client][1] = False
	ListeClient[_id_client][0].close()
	if booll:del ListeClient[_id_client]

def deco_client(_id_client):						## take in count that the client disconnect
	global ListeClient
	ListeClient[_id_client][1] = False

#################################################### Buffer gestion	###################################################

def addBuffer(_id, _msg):							## add a msg to the bufferSend for sending it
	if (ListeClient[_id][1]):
		my_send(_msg,ListeClient[_id][0])

def readBuffer():									## return the 1st msg to the BufferRecive, return None if empty
	global BufferRecive
	if len(BufferRecive) > 0 :
		temp = BufferRecive[0]
		del BufferRecive[0]
		return temp
	else:	
		return None

