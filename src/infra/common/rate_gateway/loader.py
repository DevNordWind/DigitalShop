from asyncio import Semaphore
from decimal import Decimal
from itertools import permutations

from aiocryptopay import AioCryptoPay  # type: ignore[import-untyped]

from domain.common.exchange_rate import CurrencyPair, ExchangeRate
from domain.common.money import Currency
from domain.common.port import Clock
from infra.common.rate_gateway.dto import CachedExchangeRates
from infra.common.rate_gateway.graph import ExchangeRateGraph


class CryptoPayRateLoader:
    def __init__(self, aio_cryptopay: AioCryptoPay, clock: Clock):
        self._crypto_pay: AioCryptoPay = aio_cryptopay
        self._clock: Clock = clock
        self._sem: Semaphore = Semaphore(1)

    async def load(self) -> CachedExchangeRates:
        async with self._sem:
            rates = await self._crypto_pay.get_exchange_rates()

        received_at = self._clock.now()
        graph = ExchangeRateGraph()

        for rate in rates:
            if rate.source != "USDT":
                continue

            source: Currency | None = self._normalize(rate.source)
            target: Currency | None = self._normalize(rate.target)
            if source is None or target is None:
                continue
            graph.add_rate(source, target, Decimal(str(rate.rate)))

        pairs: dict[CurrencyPair, ExchangeRate] = {}
        for source, target in set(permutations(graph.currencies(), 2)):
            rate = graph.find_rate(source, target)
            if rate is None:
                continue

            pair = CurrencyPair(source=source, target=target)
            pairs[pair] = ExchangeRate(
                pair=pair,
                rate=rate,
                timestamp=received_at,
            )
        return CachedExchangeRates(rates=pairs, received_at=received_at)

    @staticmethod
    def _normalize(currency: str) -> Currency | None:
        if currency == "USDT":
            return Currency.USD

        try:
            return Currency(currency)
        except ValueError:
            return None
