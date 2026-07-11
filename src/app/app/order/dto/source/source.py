from dataclasses import dataclass
from uuid import UUID

from app.domain.order.enums import PaymentSourceType
from app.domain.payment.enums import PaymentMethod


@dataclass(slots=True, frozen=True)
class PaymentSourceDTO:
    payment_id: UUID | None

    type: PaymentSourceType
    payment_method: PaymentMethod | None
