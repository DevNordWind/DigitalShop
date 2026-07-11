from enum import StrEnum


class CouponRedemptionStatus(StrEnum):
    RESERVED = "RESERVED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
