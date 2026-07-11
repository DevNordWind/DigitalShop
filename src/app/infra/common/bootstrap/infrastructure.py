from itertools import permutations

from dishka import AsyncContainer
from taskiq import AsyncBroker

from app.domain.common.exchange_rate import CurrencyPair, ExchangeRateGateway
from app.domain.common.money import Currency
from app.infra.framework.taskiq.tp import PriorityBroker


class InfrastructureBootstrap:
    def __init__(self, container: AsyncContainer):
        self._container = container

    async def startup(self):
        await self._load_rates()
        await self._startup_brokers()

    async def _load_rates(self) -> None:
        rates_gateway: ExchangeRateGateway = await self._container.get(
            ExchangeRateGateway
        )
        pairs: list[CurrencyPair] = [
            CurrencyPair(target=target, source=source)
            for target, source in permutations(Currency, 2)
        ]
        await rates_gateway.get_many(pairs=pairs)

    async def _startup_brokers(self) -> None:
        await self._container.get(AsyncBroker)
        await self._container.get(PriorityBroker)
