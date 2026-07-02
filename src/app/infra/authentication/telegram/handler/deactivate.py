from dataclasses import dataclass

from app.app.common.port.session import DatabaseSession
from app.infra.authentication.telegram.exception import InvalidTelegramContextError
from app.infra.authentication.telegram.model import TelegramContext, TelegramId
from app.infra.authentication.telegram.port import TelegramContextGateway


@dataclass(slots=True, frozen=True)
class DeactivateTelegramContextCmd:
    id: int


class DeactivateTelegramContext:
    def __init__(
        self,
        session: DatabaseSession,
        gateway: TelegramContextGateway,
    ):
        self._gateway = gateway
        self._session = session

    async def execute(self, cmd: DeactivateTelegramContextCmd) -> None:
        ctx: TelegramContext | None = await self._gateway.get(
            telegram_id=TelegramId(cmd.id),
        )
        if not ctx:
            raise InvalidTelegramContextError

        ctx.deactivate()
        await self._session.commit()
