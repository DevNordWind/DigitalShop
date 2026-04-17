from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class CouponId:
    value: UUID


@dataclass(slots=True, frozen=True)
class CouponRedemptionId:
    value: UUID
