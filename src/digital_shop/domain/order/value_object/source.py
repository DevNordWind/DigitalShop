from dataclasses import dataclass

from domain.order.enums import PaymentSourceType
from domain.order.exception import PaymentIdRequired
from domain.payment.value_object import PaymentId


@dataclass(slots=True, frozen=True)
class PaymentSource:
    payment_id: PaymentId | None
    type: PaymentSourceType

    def __post_init__(self) -> None:
        if self.type == PaymentSourceType.PAYMENT and self.payment_id is None:
            raise PaymentIdRequired
