from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.dto.money import MoneyDTO
from app.app.payment.dto.commission import CommissionSnapshotDTO
from app.domain.payment.enums import PaymentMethod, PaymentStatus
from app.domain.payment.value_object import PaymentPurpose


@dataclass(slots=True, frozen=True)
class PaymentDTO:
    id: UUID
    creator_id: UUID

    purpose: PaymentPurpose

    original_amount: MoneyDTO
    commission_snapshot: CommissionSnapshotDTO
    to_pay: MoneyDTO

    status: PaymentStatus

    method: PaymentMethod
    external_id: str | None

    created_at: datetime
    updated_at: datetime | None
