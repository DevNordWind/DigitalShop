from dataclasses import dataclass

from domain.payment.enums import PaymentMethod


@dataclass
class PaymentSettings:
    method: PaymentMethod
    is_active: bool
