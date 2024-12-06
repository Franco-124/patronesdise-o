from .chain_handler import ChainHandler
from src.payment_service.commons.request import Request
from .customer import CustomerValidator


class CustomerHandler(ChainHandler):
    def handle(self, request: Request):
        validator = CustomerValidator()
        try:
            valid = validator.validate(request.customer_data)
            if self._next_handler:
                self._next_handler.handle(request) if valid else print("Invalid customer data")

        except Exception as e:
            print(f"Error: {e}")
            raise e