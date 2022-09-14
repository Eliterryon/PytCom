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
    SPLIT = "!"

    message = ""
    mode = ""
    submod = ""
    author = ""

    def __init__(self, _mode="", _author="", _message="", _submod="", _raw_message=""):
        try:
            if _raw_message != "":
                _raw_message = _raw_message[1:]
                self.mode, self.submod, self.author, self.message = _raw_message.split(
                    self.SPLIT, 3
                )
                self.mode = MODE(self.mode)
                self.submod = SUB_MODE(self.submod)
            else:
                self.message = _message
                self.mode = _mode
                self.submod = _submod
                self.author = _author
        except Exception as err:
            print("error init message")
            print(err)

    def __str__(self):
        return (
            "/"
            + self.mode.value
            + self.SPLIT
            + self.submod.value
            + self.SPLIT
            + self.author
            + self.SPLIT
            + self.message
        )


if __name__ == "__main__":
    print("a")
    messagea = Message(
        _mode=MODE.MESSAGE, _author="moi", _message="connard", _submod=SUB_MODE.NULL
    )

    messageas = Message(_raw_message=str(messagea))
    print(str(messageas))
