from dataclasses import dataclass
from typing import Final
from uuid import UUID

from domain.common.money import Currency

CTX_KEY: Final[str] = "CTX"


@dataclass(slots=True)
class UsersManagementCtx:
    current_user_id: UUID | None = None

    current_top_up_currency: Currency | None = None
