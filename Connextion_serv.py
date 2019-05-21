import socket
import threading
import re
import time

HOTE = "localhost"
PORT = 15555
	
BufferSend = []
BufferRecive = []

ListeClient = {}

Connextion = True
socks = None

class myThreadRevived (threading.Thread):
	def __init__(self, _sock, _id):
		threading.Thread.__init__(self)
		self.sock = _sock
		self.id = _id
		
	def run(self):
		global ListeClient
		global BufferRecive

		while (self.id in ListeClient) and ListeClient[self.id][1]:
			try:
				temp = myrecive(self.sock.recv(255), self.sock)
				BufferRecive.append( (self.id, temp) )
			except Exception as err :
				if (self.id in ListeClient) and ListeClient[self.id][1] :
					close_connect(self.id,True)
					print(err)
					print('Recive connextion lose (' + format(self.id) + ')')
				else:
					print('Recive connextion ' + format(self.id) + ' closed')

class myThreadSend(threading.Thread):
	def __init__(self, _sock, _id):
		threading.Thread.__init__(self)
		self.sock = _sock
		self.id = _id
	
	def run(self):
		global ListeClient
		global BufferSend
		while (self.id in ListeClient) and ListeClient[self.id][1]:
			time.sleep(.05)
			if (self.id in ListeClient) and len(BufferSend) >= 1 and BufferSend[0][0] == self.id:
				try:
					my_send(BufferSend[0][1], self.sock)
					del BufferSend[0]
				except Exception as err :
					if (self.id in ListeClient) and ListeClient[self.id][1] :
						close_connect(self.id,True)
						print(err)
						print('Send connextion lose (' + format(self.id) + ')')
					else:
						print('Send connextion ' + format(self.id) + ' closed')
						del ListeClient[self.id]

class myThreadServ (threading.Thread): 
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global ListeClient
		global Connextion
		global socks


		while Connextion:
			try:				
				socks.listen(5)
				sockc, id = socks.accept()
				ListeClient[format(id)] = [sockc, True]
				lunch(sockc,format(id))
			except Exception as err :
				if Connextion :
					print(err)
					print('erreur, connextion perdu (Erreur 3)')
					Connextion = False
				else:
					Connextion = False
					print('serveur soocket closed')

def my_send(_message, _sockc):
	liste = re.findall(r".{1,200}", _message)
	temp = liste.pop()
	for i in liste :
		_sockc.send(str.encode(i+"\suit"))
	_sockc.send(str.encode(temp+"\stop"))

def myrecive(_message, _sockc):
	message = _message.decode()
	if re.match(r"(.)*(\\suit)$", message) is not None :
		temp = message[:-5] + myrecive(_sockc.recv(255))
		return (temp)
	elif re.match(r"(.)*(\\stop)$", message) is not None :
		temp = message[:-5]
		return (temp)


def lunch(_sock, _id):
	threadR = myThreadRevived(_sock, _id)
	threadS = myThreadSend(_sock, _id)
	threadR.start()
	threadS.start()
	print("client " + format(_id) + "is connected")

def stop():
	Connextion = False
	global ListeClient
	for id in ListeClient.keys():
		close_connect(id, False)
	ListeClient = {}
	socks.close()
	print("serveur closed")
	
def close_connect(_id_client, booll):
	global ListeClient
	ListeClient[_id_client][1] = False
	ListeClient[_id_client][0].close()
	if booll:del ListeClient[_id_client]

	


def connect_serveur(_hote=HOTE, _port=PORT) :
	global socks

	try:
		socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socks.bind(('', _port ))
		thread = myThreadServ()
		thread.start()
		print("connected")
		return True

	except Exception as err :
		print(err)
		print("error, can\'t opend serveur port")
		return False

def addBuffer(_id, _msg):
	BufferSend.append((_id, _msg))

def readBuffer():
	if len(BufferRecive) > 0 :
		temp = BufferRecive[0]
		del BufferRecive[0]
		return temp
	else:	
		return None

