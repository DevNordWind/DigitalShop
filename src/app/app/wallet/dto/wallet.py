from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.money import MoneyDTO
from app.domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class WalletDTO:
    id: UUID
    user_id: UUID

    currency: Currency
    balance: MoneyDTO
