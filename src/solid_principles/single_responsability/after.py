import os
from dataclasses import dataclass
import stripe
from dotenv import load_dotenv
from stripe.error import StripeError

_ = load_dotenv()  # Carga variables de entorno desde el archivo .env


@dataclass
class CustomerValidator:
    def validate(self, customer_data):
        if not customer_data.get("name"):
            print("Invalid customer data: missing name")
            raise ValueError("Invalid customer data: missing name")

        if not customer_data.get("contact_info"):
            print("Invalid customer data: missing contact info")
            raise ValueError("Invalid customer data: missing contact info")
        return True


@dataclass
class PaymentDataValidator:
    def validate(self, payment_data):
        if not payment_data.get("source"):
            print("Invalid payment data: missing source")
            raise ValueError("Invalid payment data")
        return True


class Notifier:
    def send_confirmation(self, customer_data):
        if "email" in customer_data["contact_info"]:
            from email.mime.text import MIMEText

            msg = MIMEText("Thank you for your payment.")
            msg["Subject"] = "Payment Confirmation"
            msg["From"] = "no-reply@example.com"
            msg["To"] = customer_data["contact_info"]["email"]

            print("Email sent to", customer_data["contact_info"]["email"])

        elif "phone" in customer_data["contact_info"]:
            phone_number = customer_data["contact_info"]["phone"]
            sms_gateway = "Custom SMS Gateway"
            print(f"SMS sent to {phone_number}: Thank you for your payment.")


@dataclass
class TransactionLogger:
    def log(self, customer_data, payment_data, charge):
        with open("transactions.log", "a") as log_file:
            log_file.write(f"{customer_data['name']} paid {payment_data['amount']} cents\n")
            log_file.write(f"Payment status: {charge['status']}\n")


@dataclass
class StripePaymentProcessor:
    def process_transaction(self, customer_data, payment_data):
        stripe.api_key = os.getenv("STRIPE_API_KEY")

        try:
            charge = stripe.Charge.create(
                amount=payment_data["amount"],
                currency="usd",
                source=payment_data["source"],
                description=f"Charge for {customer_data['name']}",
            )
            print("Payment successful")
            return charge
        except StripeError as e:
            print("Payment failed:", e)
            raise e


@dataclass
class PaymentService:
    customer_validator = CustomerValidator()
    payment_data_validator = PaymentDataValidator()
    payment_processor = StripePaymentProcessor()
    notifier = Notifier()
    logger = TransactionLogger()

    def process_transaction(self, customer_data, payment_data)-> stripe.Charge:
        self.customer_validator.validate(customer_data)
        self.payment_data_validator.validate(payment_data)

        try:
            charge = self.payment_processor.process_transaction(customer_data, payment_data)
            self.notifier.send_confirmation(customer_data)
            self.logger.log(customer_data, payment_data, charge)
            return charge
        except StripeError as e:
            print("Payment failed:", e)
            raise e
        

if __name__ == "__main__":
    payment_service = PaymentService()

    customer_data_with_email = {
        "name": "John Doe",
        "contact_info": {"email": "e@mail.com"},
    }

    customer_data_with_phone = {
        "name": "Platzi Python",
        "contact_info": {"phone": "1234567890"},
    }

    """payment_data = {"amount": 500, "source": "tok_mastercard"}

    # Procesar transacciones
    payment_service.process_transaction(customer_data_with_email, payment_data)
    payment_service.process_transaction(customer_data_with_phone, payment_data)"""
    
    payment_data = {"amount": 700, "source": "tok_radarBlock", "cvv": 123}
    try: 
        payment_service.process_transaction(customer_data_with_email, payment_data)
    except ValueError as e:
        print("Error con el procesamiento:", e)