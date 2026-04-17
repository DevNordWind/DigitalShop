from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.port import DatabaseSession
from app.product.position.exception import PositionNotFound
from app.user.service import GetCurrentUser
from domain.common.exchange_rate import CurrencyPair, ExchangeRateGateway
from domain.common.money import Currency, Money
from domain.common.port import Clock
from domain.product.position.entity import Position
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService
from domain.product.position.value_object import PositionId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class ConvertPositionPriceToOthersCmd:
    id: UUID


class ConvertPositionPriceToOthers:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        rate_gateway: ExchangeRateGateway,
        current_user: GetCurrentUser,
        clock: Clock,
    ):
        self._repository: PositionRepository = repository
        self._session: DatabaseSession = session
        self._rate_gateway: ExchangeRateGateway = rate_gateway
        self._current_user: GetCurrentUser = current_user
        self._clock: Clock = clock

    async def __call__(self, cmd: ConvertPositionPriceToOthersCmd) -> None:
        editor: User = await self._current_user()

        if not PositionAccessService.can_edit(editor_role=editor.role):
            raise PositionPermissionDenied

        position: Position | None = await self._repository.get_for_update(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFound

        source: Money = position.price.get_default()

        pairs = [
            CurrencyPair(source=source.currency, target=currency)
            for currency in Currency
            if currency != source.currency
        ]

        rates = await self._rate_gateway.get_many(pairs)

        now: datetime = self._clock.now()

        for rate in rates:
            position.set_price(price=rate.convert(source), now=now)

        await self._session.commit()
