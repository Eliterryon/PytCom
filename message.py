from enum import Enum

class MODE(Enum):
	MESSAGE = "m"
	SETTING = "t"
	CONNECTION = "c"
	SALON = "s"
	PRIVAT_MESSAGE = "p"
	CLOSING = "e"

class SUB_MODE(Enum):
	ADDITION = "+"
	SUBSTRACTION = "-"
	INITIALISATION = "i"
	MODIFICATION = "m"
	NULL = ""


class Message:

	message = ""
	mode = ""
	submod = ""
	author = ""
	
	def __init__(self, _mode, _author, _message, _submod = ""):
		self.message = _message
		self.mode = _mode
		self.submod = _submod
		self.author = _author
	
	def __init__(self, _raw_message):
		self.mode, reste= _raw_message.split(" ", 1)
		self.mode = self.mode[1:]
		if self.mode == "\\c":
			self.submod, reste = reste.split(" ", 1)
		elif self.mode == "\\s":
			self.submod, reste = reste.split(" ", 1)
		elif self.mode == "\\m":
			self.submod, reste = reste.split(" ", 1)

		self.submod = SUB_MODE(self.submod)
		self.mode = MODE(self.mode)

		self.author, self.message = reste.split(" ", 1)

	def tostring(self):
		if(self.submod == ""):
			return "/"+ self.mode + " " + self.message
		return "/"+ self.mode + " " + self.submod + " " + self.message