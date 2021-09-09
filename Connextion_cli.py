import socket
import threading
import re
import time
import Observeur 

HOTE = "localhost"
PORT = 15555
	
BufferRecive = []									## buffer for recived message : [msg]

ObserverRecive = Observeur.Observer()

Connextion = True
sock = None


################################################ thread client side	###############################################

class myThreadRevived (threading.Thread):			## thraed who wait a upcomming message
	def __init__(self, _sock):
		threading.Thread.__init__(self)
		self.sock = _sock
		self.sock.settimeout(2)
		
	def run(self):
		global Connextion
		global BufferRecive

		while Connextion:
			try:
				temp = myrecive(self.sock.recv(255))
				BufferRecive.append(temp)
				ObserverRecive.notify(readBuffer())
			except socket.timeout:
				pass
			except Exception as err :
				if Connextion :
					Connextion = False #TODO
					print(err)
					print('Recive connextion lose (Erreur 1)')
				else:
					print('Recive connextion closed')
	

################################################### message gestion	###################################################

def my_send(_message):								## cut and send leaving msg
	global sock
	liste = re.findall(r'.{1,200}', _message)
	temp = liste.pop()
	for i in liste :
		sock.send(str.encode(i+"\suit"))
	sock.send(str.encode(temp+"\stop"))

def myrecive(_message):								## recive and concaten upcomming msg 
	global sock
	message = _message.decode()
	if re.match(r"(.)*(\\suit)$", message) is not None :
		return (message[:-5] + myrecive(sock.recv(255)))
	elif re.match(r"(.)*(\\stop)$", message) is not None :
		return message[:-5]

########################################## serveux client connextion gestion ###########################################

def connect_client(ObserverReciveFonction = None, _hote=HOTE, _port=PORT) :
	global sock
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.connect((_hote, _port))
		lunch(sock, ObserverReciveFonction)
		print("connected")
		return True
	except Exception as err :
		close_connect()
		print(err)
		print("error, can\'t opend serveur port (Erreur 2)")
		return False

def close_connect():
	global sock
	global Connextion
	Connextion = False
	sock.close()
	time.sleep(.06)
	print("client closed")

#################################################### Buffer gestion	###################################################

def addBuffer(_msg):
	my_send(_msg)


def readBuffer():
	if len(BufferRecive) > 0 :
		temp = BufferRecive[0]
		del BufferRecive[0]
		return temp
	else:	
		return None



#################################################### Lunch ############################################################


def lunch(_sock, ObserverReciveFonction = None):

	global ObserverRecive

	threadR = myThreadRevived(_sock)
	threadR.name = "myThreadRevived"
	ObserverRecive.attach(ObserverReciveFonction)
	
	threadR.start()
