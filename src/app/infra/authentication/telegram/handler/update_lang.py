from dataclasses import dataclass

from app.app.common.port.session import DatabaseSession
from app.domain.common.localized import Language
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.infra.authentication.telegram.exception import InvalidTelegramContextError
from app.infra.authentication.telegram.model import TelegramContext, TelegramId
from app.infra.authentication.telegram.port import TelegramContextGateway


@dataclass(slots=True, frozen=True)
class UpdateTelegramLangCmd:
    new_lang: Language


class UpdateTelegramLangHandler:
    def __init__(
        self,
        current_context: TelegramContextDTO,
        session: DatabaseSession,
        gateway: TelegramContextGateway,
    ):
        self._ctx = current_context
        self._gateway = gateway
        self._session = session

    async def execute(self, data: UpdateTelegramLangCmd) -> None:
        context: TelegramContext | None = await self._gateway.get(
            telegram_id=TelegramId(self._ctx.id),
        )
        if not context:
            raise InvalidTelegramContextError

        context.lang = data.new_lang

        return await self._session.commit()
