from dataclasses import dataclass

from app.user.exception import UserAuthenticationError
from domain.common.money import Currency
from infra.authentication.telegram.dto import TelegramContextDTO
from infra.authentication.telegram.model import TelegramContext, TelegramId
from infra.authentication.telegram.port import (
    NonExpiringSession,
    TelegramContextGateway,
)


@dataclass(slots=True, frozen=True)
class UpdateTelegramCurrencyCmd:
    new_currency: Currency


class UpdateTelegramCurrency:
    def __init__(
        self,
        current_context: TelegramContextDTO,
        session: NonExpiringSession,
        gateway: TelegramContextGateway,
    ):
        self._ctx: TelegramContextDTO = current_context
        self._gateway: TelegramContextGateway = gateway
        self._session: NonExpiringSession = session

    async def execute(self, data: UpdateTelegramCurrencyCmd) -> None:
        context: TelegramContext | None = await self._gateway.get(
            telegram_id=TelegramId(self._ctx.id),
        )
        if not context:
            raise UserAuthenticationError

        context.currency = data.new_currency

        return await self._session.commit()
