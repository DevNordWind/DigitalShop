from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PaymentExternalId:
    value: str
