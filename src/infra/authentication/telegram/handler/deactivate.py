from dataclasses import dataclass

from infra.authentication.telegram.exception import InvalidTelegramContext
from infra.authentication.telegram.model import TelegramContext, TelegramId
from infra.authentication.telegram.port import (
    NonExpiringSession,
    TelegramContextGateway,
)


@dataclass(slots=True, frozen=True)
class DeactivateTelegramContextCmd:
    id: int


class DeactivateTelegramContext:
    def __init__(
        self,
        session: NonExpiringSession,
        gateway: TelegramContextGateway,
    ):
        self._gateway: TelegramContextGateway = gateway
        self._session: NonExpiringSession = session

    async def execute(self, cmd: DeactivateTelegramContextCmd) -> None:
        ctx: TelegramContext | None = await self._gateway.get(
            telegram_id=TelegramId(cmd.id),
        )
        if not ctx:
            raise InvalidTelegramContext

        ctx.deactivate()
        await self._session.commit()
