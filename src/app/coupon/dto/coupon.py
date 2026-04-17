from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.coupon.dto.discount import DiscountDTO


@dataclass(slots=True, frozen=True)
class CouponDTO:
    id: UUID
    creator_id: UUID

    code: str
    discount: DiscountDTO

    valid_from: datetime
    valid_until: datetime | None

    created_at: datetime

    is_revoked: bool
