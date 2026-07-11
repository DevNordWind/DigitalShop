from dataclasses import dataclass

from app.domain.order.enums import PaymentSourceType
from app.domain.order.exception import PaymentIdRequiredError
from app.domain.payment.value_object import PaymentId


@dataclass(slots=True, frozen=True)
class PaymentSource:
    payment_id: PaymentId | None
    type: PaymentSourceType

    def __post_init__(self) -> None:
        if self.type == PaymentSourceType.PAYMENT and self.payment_id is None:
            raise PaymentIdRequiredError
