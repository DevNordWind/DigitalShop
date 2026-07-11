from dataclasses import dataclass

from aiocryptopay import Networks


@dataclass(slots=True, frozen=True)
class CryptoPayConfig:
    token: str
    network: Networks


@dataclass(slots=True, frozen=True)
class PaymentConfig:
    crypto_pay: CryptoPayConfig
