from abc import ABC, abstractmethod
from typing import self, Optional

from commons import request

class ChainHandler(ABC):
    _next_handler: Optional[self]= None


    def set_next(self, handler: self):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: request):
        ...

    def next(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None