from dataclasses import dataclass
from uuid import UUID

from app.domain.payment.enums import PaymentPurposeType


@dataclass(slots=True, frozen=True)
class PaymentPurpose:
    reference_id: UUID
    type: PaymentPurposeType
