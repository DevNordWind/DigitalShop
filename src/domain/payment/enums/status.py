from enum import StrEnum


class PaymentStatus(StrEnum):
    NEW = "NEW"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
