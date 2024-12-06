from decorator_protocol import payment_service_decorator_protocol
from dataclasses import dataclass
from typing import Optional,self

from .commons import CustomerData, PaymentData, PaymentResponse

from service_protocol import PaymentServiceProtocol
from typing import Protocol

class PaymentServiceLoggig(payment_service_decorator_protocol):
    wrapped : payment_service_decorator_protocol
    


    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        print("Star procces transaction")
        response = self.wrapped.process_transaction(customer_data, payment_data)
        print("finish procces transaction")     
        return response 
    def process_refund(self, transaction_id: str):
        print("Star procces refund")
        response = self.wrapped.process_refund(transaction_id)
        print("Finish procces refund")
        return response
    
    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ):
        print("Star setup recurring")

        print("Finish setup recurring") 
    