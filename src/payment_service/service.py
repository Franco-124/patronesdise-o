from dataclasses import dataclass
from typing import Optional, self

from .commons import CustomerData, PaymentData,request, PaymentResponse
from .loggers import TransactionLogger
from .notifiers import NotifierProtocol
from .processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProcessorProtocol,
    RefundProcessorProtocol,
)
from .validators import CustomerValidator, PaymentDataValidator
from listeners.listener import Listenermanager
from factory import PaymentProcessorFactory

from validators import chain_handler

@dataclass
class PaymentService:
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol
    """customer_validator: CustomerValidator
    payment_validator: PaymentDataValidator"""
    validators : chain_handler
    Listeners: Listenermanager
    logger: TransactionLogger
    refund_processor: Optional[RefundProcessorProtocol] = None
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None

    def set_notifier(self, notifier: NotifierProtocol):
        print("Changing the notifier implementation")
        self.notifier = notifier



    @classmethod
    def create_with_payment_proccesor(
        cls, payment_data: PaymentData,  **kwargs
        )->self:
        try:
            proccesor = PaymentProcessorFactory.get_payment_processor(
                payment_data
                )
            return cls(payment_processor=proccesor, **kwargs)
        
        except ValueError as e:
            print("Error creando la clase")
            raise e



    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        """ self.customer_validator.validate(customer_data)
        self.payment_validator.validate(payment_data)"""
        try:
            request = request(customer_data, payment_data)
            self.validators.handle(request = request)
        except Exception as e:
            print("Fallo en las validaciones", e)
            raise e
        
        payment_response = self.payment_processor.process_transaction(
            customer_data, payment_data
        )
        self.Listeners.notifyAll(f"Pago exitoso al evento de tipo evento {payment_response}")
        self.notifier.send_confirmation(customer_data)
        self.logger.log_transaction(
            customer_data, payment_data, payment_response
        )
        return payment_response

    def process_refund(self, transaction_id: str):
        if not self.refund_processor:
            raise Exception("this processor does not support refunds")
        refund_response = self.refund_processor.refund_payment(transaction_id)
        self.logger.log_refund(transaction_id, refund_response)
        return refund_response

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ):
        if not self.recurring_processor:
            raise Exception("this processor does not support recurring")
        recurring_response = self.recurring_processor.setup_recurring_payment(
            customer_data, payment_data
        )
        self.logger.log_transaction(
            customer_data, payment_data, recurring_response
        )
        return recurring_response
