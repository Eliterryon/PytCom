import socket
import threading
import re
import time
import observeur 

HOTE = "localhost"
PORT = 15555
SIZE_MESSAGE = r'.{1,200}'
	
BufferRecive = []									## buffer for recived message : [msg]

ObserverRecive = observeur.Observer()

Connexion = True
sock = None


################################################ thread client side	###############################################

class myThreadRevived (threading.Thread):			## thraed who wait a upcomming message
	def __init__(self, _sock):
		threading.Thread.__init__(self)
		self.sock = _sock
		self.sock.settimeout(2)
		
	def run(self):
		global Connexion
		global BufferRecive

		while Connexion:
			try:
				temp = self.sock.recv(255)
			except socket.timeout:
				pass
			except Exception as err :
				if Connexion :
					Connexion = False #TODO
					print(err)
					print('Recive connexion lose (Erreur 1)')
				else:
					print('Recive connexion closed')
			else:
				temp = custom_recive(temp)
				BufferRecive.append(temp)
				ObserverRecive.notify(readBuffer())
	

################################################### message gestion	###################################################

def custom_send(_message):								## cut and send leaving msg
	global sock
	liste = re.findall(SIZE_MESSAGE, _message)
	temp = liste.pop()
	for i in liste :
		sock.send(str.encode(i+"\suit"))
	sock.send(str.encode(temp+"\stop"))

def custom_recive(_message):								## recive and concaten upcomming msg 
	global sock
	tempMessage = _message.decode()
	if re.match(r"(.)*(\\suit)$", tempMessage) is not None :
		return (tempMessage[:-5] + custom_recive(sock.recv(255)))
	elif re.match(r"(.)*(\\stop)$", tempMessage) is not None :
		return tempMessage[:-5]

########################################## serveux client connexion gestion ###########################################

def connect_client(_observerReciveFonction = None, _hote=HOTE, _port=PORT) :
	global sock
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.connect((_hote, _port))
		lunch(sock, _observerReciveFonction)
		print("connected")
		return True
	except Exception as err :
		close_connect()
		print(err)
		print("error, can\'t opend serveur port (Erreur 2)")
		return False

def close_connect():
	global sock
	global Connexion
	Connexion = False
	sock.close()
	time.sleep(.06)
	print("client closed")

#################################################### Buffer gestion	###################################################

def addBuffer(_msg):
	custom_send(_msg)


def readBuffer():
	if len(BufferRecive) > 0 :
		temp = BufferRecive[0]
		del BufferRecive[0]
		return temp
	else:	
		return None



#################################################### Lunch ############################################################


def lunch(_sock, _observerReciveFonction = None):

	global ObserverRecive

	threadR = myThreadRevived(_sock)
	threadR.name = "myThreadRevived"
	ObserverRecive.attach(_observerReciveFonction)
	
	threadR.start()
