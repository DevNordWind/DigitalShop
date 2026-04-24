from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain.common.localized import Language
from domain.user.value_object import UserId
from infra.authentication.telegram.dto import TelegramContextData
from infra.authentication.telegram.model import TelegramContext, TelegramId


class TelegramContextGateway(ABC):
    @abstractmethod
    async def save(self, context: TelegramContext) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_data(
        self, telegram_id: TelegramId
    ) -> TelegramContextData | None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, telegram_id: TelegramId) -> TelegramContext | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: UserId) -> TelegramContext | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_id(self, telegram_id: TelegramId) -> UserId | None:
        raise NotImplementedError

    @abstractmethod
    async def get_lang(self, telegram_id: TelegramId) -> Language | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        is_active: bool | None = None,
    ) -> list[TelegramContext]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_langs(
        self, langs: Sequence[Language], is_active: bool | None = None
    ) -> list[TelegramContext]:
        raise NotImplementedError

    @abstractmethod
    async def get_admins(
        self,
        is_active: bool | None = None,
    ) -> list[TelegramContext]:
        raise NotImplementedError
