class Observer:
    def __init__(self):
        self._observers = []

    def notify(self, *arg):
        for observer in self._observers:
            observer.update(arg)

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
