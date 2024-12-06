from dataclasses import dataclass
from typing import Optional, self
from service import PaymentService
from .commons import CustomerData, PaymentData, PaymentResponse
from .loggers import TransactionLogger
from .notifiers import NotifierProtocol, EmailNotifier, SMSNotifier
from .processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProcessorProtocol,
    RefundProcessorProtocol,

)
from factory import PaymentProcessorFactory
from .validators import CustomerValidator, PaymentDataValidator

@dataclass
class PaymentServiceBuilder:
    payment_processor:Optional[ PaymentProcessorProtocol]=None
    notifier: Optional[NotifierProtocol]=None
    customer_validator: Optional[CustomerValidator]=None
    payment_validator: Optional[PaymentDataValidator]=None
    logger: Optional[TransactionLogger]=None
    refund_processor: Optional[RefundProcessorProtocol] = None
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None
    
    def set_logger(self) ->self:
        self.logger = TransactionLogger()
        return self
    
    def set_Payment_validation(self) ->self:
        self.payment_validator = PaymentDataValidator()
        return self
    
    def set_customer_validation(self) ->self:
        self.customer_validator = CustomerValidator()
        return self 
    
    def set_payment_proccesor(self , payment_data: PaymentData)->self:
        self.payment_processor = PaymentProcessorFactory.get_payment_processor(
            payment_data
            )
        return self
    
    def set_notifier(self, customer_data: CustomerData)->self:
        if customer_data.contact_email:
            self.notifier = EmailNotifier()
            return self
        
        if customer_data.contact_info.phone:
            self.notifier = SMSNotifier(gateway="MycustomGateway")
            return self
        raise ValueError("No se puede elegir la estrategia correcta")
    

    def build(self):
        if not all([
            self.payment_processor,
            self.notifier,
            self.customer_validator,
            self.payment_validator
            ]):

            missing = [
                name
                for name,value in [
                    ("payment_processor", self.payment_processor),
                    ("notifier", self.notifier),
                    ("customer_validator", self.customer_validator),
                    ("payment_validator", self.payment_validator),
                    ("logger", self.logger)
                    ]
                    if value is None
            ]
            raise ValueError(f"Missing fields: {missing}")
                     
        return PaymentService(
            payment_processor=self.payment_processor,#type ignore
            notifier=self.notifier,
            customer_validator=self.customer_validator,
            payment_validator=self.payment_validator,
            notifier=self.notifier,
            logger=self.logger,
           
        )


        