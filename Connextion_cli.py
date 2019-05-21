import socket
import threading
import re
import time

HOTE = "localhost"
PORT = 15555
	
BufferSend = []
BufferRecive = []

Connextion = True
sock = None

class myThreadRevived (threading.Thread):
	def __init__(self, _sock):
		threading.Thread.__init__(self)
		self.sock = _sock
		
	def run(self):
		global Connextion
		global BufferRecive

		while Connextion:
			try:
				temp = myrecive(self.sock.recv(255))
				BufferRecive.append(temp)

			except Exception as err :
				if Connextion :
					Connextion = False #TODO
					print(err)
					print('Recive connextion lose ')
				else:
					print('Recive connextion closed')
	
class myThreadSend(threading.Thread):
	def __init__(self, _sock):
		threading.Thread.__init__(self)
		self.sock = _sock
	
	def run(self):
		global Connextion
		global BufferSend

		while Connextion:
			time.sleep(.05)
			if len(BufferSend) >= 1 :
				try:
					my_send(BufferSend[0])
					del BufferSend[0]
				except Exception as err :
					Connextion = False #TODO
					print(err)
					print('Send connextion lose ')
		print('Send connextion closed')

def my_send(_message):
	global sock
	liste = re.findall(r'.{1,200}', _message)
	temp = liste.pop()
	for i in liste :
		sock.send(str.encode(i+"\suit"))
	sock.send(str.encode(temp+"\stop"))

def myrecive(_message):
	global sock
	message = _message.decode()
	if re.match(r"(.)*(\\suit)$", message) is not None :
		return (message[:-5] + myrecive(sock.recv(255)))
	elif re.match(r"(.)*(\\stop)$", message) is not None :
		return message[:-5]

def lunch(_sock):
	threadR = myThreadRevived(_sock)
	threadS = myThreadSend(_sock)
	threadR.start()
	threadS.start()

def close_connect():
	global sock
	global Connextion
	Connextion = False
	sock.close()
	time.sleep(.06)
	print("client closed")


def connect_client(_hote=HOTE, _port=PORT) :
	global sock
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.connect((_hote, _port))
		lunch(sock)
		print("connected")
		return True
		
	except Exception as err :
		close_connect()
		print(err)
		print("error, can\'t opend serveur port")
		return False

def addBuffer(_msg):
	BufferSend.append(_msg)

def readBuffer():
	if len(BufferRecive) > 0 :
		temp = BufferRecive[0]
		del BufferRecive[0]
		return temp
	else:	
		return None