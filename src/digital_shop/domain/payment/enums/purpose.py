from enum import StrEnum


class PaymentPurposeType(StrEnum):
    WALLET_TOP_UP = "WALLET_TOP_UP"
    ORDER_PAYMENT = "ORDER_PAYMENT"
