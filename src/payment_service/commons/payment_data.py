from pydantic import BaseModel
from enum import Enum

class PaymentType(BaseModel):
    OFFLINE = "offline"
    ONLINE = "online"


class PaymentData(BaseModel):
    ammount = int
    source = str
    currency : str = "USD"
    type:PaymentType = PaymentType.ONLINE



