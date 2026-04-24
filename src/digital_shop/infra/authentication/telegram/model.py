from dataclasses import dataclass
from typing import NewType

from domain.common.localized import Language
from domain.common.money import Currency
from domain.user.value_object import UserId

TelegramId = NewType("TelegramId", int)


@dataclass
class TelegramContext:
    id: TelegramId

    user_id: UserId

    tg_username: str | None
    tg_first_name: str

    lang: Language | None
    currency: Currency

    is_active: bool

    def deactivate(self) -> None:
        self.is_active = False

    def sync_data(
        self,
        tg_first_name: str,
        tg_username: str | None = None,
    ) -> None:
        if self.tg_username != tg_username:
            self.tg_username = tg_username

        if self.tg_first_name != tg_first_name:
            self.tg_first_name = tg_first_name

        if not self.is_active:
            self.is_active = True
