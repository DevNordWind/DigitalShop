from dataclasses import dataclass
from typing import Final
from uuid import UUID

from app.payment.port.payment import Invoice

CTX_KEY: Final[str] = "CTX_KEY"


@dataclass(slots=True)
class OrderCtx:
    order_id: UUID

    invoice: Invoice | None = None
