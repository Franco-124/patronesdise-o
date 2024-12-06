from listener import Listener
from dataclasses import dataclass,field


class ListenerManager[T]:

    listeners: list[Listener] = field(default_factory=list)

    def subscribe(self, Listener: Listener):
        self.listeners.append(Listener)
    

    def unsiscribe(self,Listener):
        self.listeners.remove(Listener)

    
    def notifyAll(self, event:T):
        for listener in self.listeners:
            listener.notify(event)