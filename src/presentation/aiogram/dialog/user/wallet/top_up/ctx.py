from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from app.payment.port.payment import Invoice
from domain.common.money import Currency

CTX_KEY: Final[str] = "CTX"


@dataclass(slots=True)
class TopUpCtx:
    current_currency: Currency

    top_up_amount: Decimal | None = None
    invoice: Invoice | None = None
