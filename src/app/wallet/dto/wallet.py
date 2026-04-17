from dataclasses import dataclass
from uuid import UUID

from app.common.dto.money import MoneyDTO
from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class WalletDTO:
    id: UUID
    user_id: UUID

    currency: Currency
    balance: MoneyDTO
