from enum import StrEnum


class CouponStatus(StrEnum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    NOT_STARTED = "NOT_STARTED"
