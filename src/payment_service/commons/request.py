from .payment_data import PaymentData
from pydantic import BaseModel
from .customer import CustomerData

class Request(BaseModel):
    customer_data: CustomerData
    payment_data: PaymentData