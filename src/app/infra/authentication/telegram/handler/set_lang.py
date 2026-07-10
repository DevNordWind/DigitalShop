from dataclasses import dataclass
from typing import Final

from frozendict import frozendict

from app.app.common.port.session import DatabaseSession
from app.domain.common.localized import Language
from app.domain.common.money import Currency
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.infra.authentication.telegram.exception import InvalidTelegramContextError
from app.infra.authentication.telegram.model import TelegramContext, TelegramId
from app.infra.authentication.telegram.port import TelegramContextGateway

_CURRENCY_TABLE: frozendict[Language, Currency] = frozendict(
    {Language.RU: Currency.RUB, Language.EN: Currency.USD, Language.UK: Currency.UAH}
)
_FALLBACK_CURRENCY: Final[Currency] = Currency.RUB


@dataclass(slots=True, frozen=True)
class SetTelegramLangCmd:
    lang: Language


class SetTelegramLangHandler:
    """Used during the initial language selection"""

    def __init__(
        self,
        current_context: TelegramContextDTO,
        session: DatabaseSession,
        gateway: TelegramContextGateway,
    ):
        self._ctx = current_context
        self._gateway = gateway
        self._session = session

    async def execute(self, data: SetTelegramLangCmd) -> None:
        context: TelegramContext | None = await self._gateway.get(
            telegram_id=TelegramId(self._ctx.id),
        )
        if not context:
            raise InvalidTelegramContextError

        context.lang = data.lang
        context.currency = _CURRENCY_TABLE.get(data.lang, _FALLBACK_CURRENCY)

        return await self._session.commit()
