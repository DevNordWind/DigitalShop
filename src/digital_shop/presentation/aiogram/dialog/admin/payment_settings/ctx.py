from dataclasses import dataclass
from typing import Final

from domain.payment.enums import PaymentMethod

CTX_KEY: Final[str] = "CTX_KEY"


@dataclass(slots=True)
class PaymentSettingsCtx:
    current_method: PaymentMethod | None = None
