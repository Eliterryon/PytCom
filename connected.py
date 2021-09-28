import Identificator 

class Connected:
	name = ""
	uid = 0

	def __init__(self, _name = ""):
		self.name = _name
		self.uid = Identificator.givID()