from dataclasses import dataclass
from uuid import UUID

from domain.common.localized import Language
from domain.common.money import Currency
from domain.user.enums import UserRole
from infra.authentication.telegram.model import TelegramContext


@dataclass(slots=True, frozen=True)
class TelegramContextData:
    ctx: TelegramContext
    role: UserRole


@dataclass(slots=True, frozen=True)
class TelegramContextDTO:
    id: int

    user_id: UUID
    user_role: UserRole

    tg_username: str | None
    tg_first_name: str

    lang: Language | None
    currency: Currency

    is_active: bool
