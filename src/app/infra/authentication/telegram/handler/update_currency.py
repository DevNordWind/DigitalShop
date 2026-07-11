from dataclasses import dataclass

from app.app.common.port.session import DatabaseSession
from app.domain.common.money import Currency
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.infra.authentication.telegram.exception import InvalidTelegramContextError
from app.infra.authentication.telegram.model import TelegramContext, TelegramId
from app.infra.authentication.telegram.port import TelegramContextGateway


@dataclass(slots=True, frozen=True)
class UpdateTelegramCurrencyCmd:
    new_currency: Currency


class UpdateTelegramCurrency:
    def __init__(
        self,
        current_context: TelegramContextDTO,
        session: DatabaseSession,
        gateway: TelegramContextGateway,
    ):
        self._ctx = current_context
        self._gateway = gateway
        self._session = session

    async def execute(self, data: UpdateTelegramCurrencyCmd) -> None:
        context: TelegramContext | None = await self._gateway.get(
            telegram_id=TelegramId(self._ctx.id),
        )
        if not context:
            raise InvalidTelegramContextError

        context.currency = data.new_currency

        return await self._session.commit()
