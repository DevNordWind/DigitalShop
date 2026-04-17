from dataclasses import dataclass
from uuid import UUID

from app.common.dto.money import MoneyDTO


@dataclass(frozen=True, slots=True)
class AppliedCouponDTO:
    coupon_id: UUID
    discount: MoneyDTO
