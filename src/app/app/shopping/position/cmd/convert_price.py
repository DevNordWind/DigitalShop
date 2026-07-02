from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.exchange_rate import CurrencyPair, ExchangeRateGateway
from app.domain.common.money import Currency, Money
from app.domain.common.port import Clock
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class ConvertPositionPriceToOthersCmd:
    id: UUID


class ConvertPositionPriceToOthers:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        rate_gateway: ExchangeRateGateway,
        actor_provider: ActorProvider,
        clock: Clock,
    ):
        self._repository = repository
        self._session = session
        self._rate_gateway = rate_gateway
        self._actor_provider = actor_provider
        self._clock = clock

    async def __call__(self, cmd: ConvertPositionPriceToOthersCmd) -> None:
        PositionAccessService.ensure_can_edit(actor=await self._actor_provider.get())

        position: Position | None = await self._repository.acquire(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFoundError

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
