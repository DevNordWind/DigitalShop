from contextlib import suppress
from uuid import UUID

from app.user.port import UserIdentifyResolver
from domain.user.value_object import UserId
from infra.authentication.telegram.model import TelegramId
from infra.authentication.telegram.port import TelegramContextGateway


class TelegramIdentifyResolver(UserIdentifyResolver):
    def __init__(self, gateway: TelegramContextGateway):
        self._gw: TelegramContextGateway = gateway

    async def resolve(self, identifier: str | UUID) -> UserId | None:
        if isinstance(identifier, UUID):
            return UserId(value=identifier)

        with suppress(ValueError):
            return UserId(value=UUID(identifier))

        try:
            tg_identifier: TelegramId = TelegramId(int(identifier))
        except ValueError:
            return None

        return await self._gw.get_user_id(telegram_id=tg_identifier)
