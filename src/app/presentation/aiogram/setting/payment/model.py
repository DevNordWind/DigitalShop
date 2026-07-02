from dataclasses import dataclass

from app.domain.payment.enums import PaymentMethod


@dataclass(slots=True)
class PaymentSettings:
    method: PaymentMethod
    is_active: bool

    def switch_status(self) -> None:
        self.is_active = not self.is_active
