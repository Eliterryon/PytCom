from email import message
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
    NULL = "0"


class Message:

    message = ""
    mode = ""
    submod = ""
    author = ""

    def __init__(self, _mode="", _author="", _message="", _submod="", _raw_message=""):
        try:
            if _raw_message != "":
                self.mode = MODE(_raw_message[1:2])
                self.submod = SUB_MODE(_raw_message[3:4])
                self.message = _raw_message[5:]

            else:
                self.message = _message
                self.mode = _mode
                self.submod = _submod
                self.author = _author
        except Exception as err:
            print("error init message")
            print(err)

    def __str__(self):
        if self.submod == "":
            return "/" + self.mode + " " + self.message
        return "/" + self.mode.value + " " + self.submod.value + " " + self.message


if __name__ == "__main__":
    print("a")
    messagea = Message(
        _mode=MODE.MESSAGE, _author="moi", _message="connard", _submod=SUB_MODE.NULL
    )
    print(str(messagea))
