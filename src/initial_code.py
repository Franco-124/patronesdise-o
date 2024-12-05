import os
from dotenv import load_dotenv
import stripe
from stripe.error import StripeError
from email.mime.text import MIMEText

# Cargar variables de entorno
load_dotenv()

# Configurar clave de Stripe
stripe.api_key = os.getenv("STRIPE_API_KEY")


class PaymentProcessor:
    def process_transaction(self, customer_data, payment_data):
        # Validación de datos del cliente
        if not customer_data.get("name"):
            print("Invalid customer data: missing name")
            return
        if not customer_data.get("contact_info"):
            print("Invalid customer data: missing contact info")
            return
        if not payment_data.get("source"):
            print("Invalid payment data")
            return

        # Procesar el pago
        try:
            charge = stripe.Charge.create(
                amount=payment_data["amount"],
                currency="usd",
                source=payment_data["source"],
                description="Charge for " + customer_data["name"],
            )
            print("Payment successful")
        except StripeError as e:
            print("Payment failed:", e)
            return

        # Notificar al cliente por email o SMS
        if "email" in customer_data["contact_info"]:
            self.send_email(customer_data["contact_info"]["email"])
        elif "phone" in customer_data["contact_info"]:
            self.send_sms(customer_data["contact_info"]["phone"])
        else:
            print("No valid contact information for notification")
            return

        # Registrar la transacción
        self.log_transaction(customer_data["name"], payment_data["amount"], charge["status"])

    def send_email(self, email):
        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = email
        print(f"Email simulated to {email}")

    def send_sms(self, phone_number):
        print(f"SMS simulated to {phone_number}: Thank you for your payment.")

    def log_transaction(self, name, amount, status):
        with open("transactions.log", "a") as log_file:
            log_file.write(f"{name} paid {amount}\n")
            log_file.write(f"Payment status: {status}\n")


if __name__ == "__main__":
    payment_processor = PaymentProcessor()

    customer_data_with_email = {
        "name": "John Doe",
        "contact_info": {"email": "e@mail.com"},
    }
    customer_data_with_phone = {
        "name": "Platzi Python",
        "contact_info": {"phone": "1234567890"},
    }

    payment_data = {"amount": 500, "source": "tok_mastercard"}

    payment_processor.process_transaction(customer_data_with_email, payment_data)
    payment_processor.process_transaction(customer_data_with_phone, payment_data)
