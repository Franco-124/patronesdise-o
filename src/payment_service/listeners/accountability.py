from .listener import Listener

class AccountabilityListener[T](Listener):

    def notify(self, event):
        print(f"AccountabilityListener notified of event: {event}")
        