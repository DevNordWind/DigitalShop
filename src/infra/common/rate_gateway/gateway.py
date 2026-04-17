import logging
from collections.abc import Sequence
from datetime import timedelta

from aiocryptopay.exceptions import (  # type: ignore[import-untyped]
    CodeErrorFactory,
)

from domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRate,
    ExchangeRateGateway,
    ExchangeRateNotFound,
)
from domain.common.port import Clock
from infra.common.rate_gateway.cache import ExchangeRateCache
from infra.common.rate_gateway.dto import CachedExchangeRates
from infra.common.rate_gateway.loader import CryptoPayRateLoader

logger = logging.getLogger(__name__)


class CryptoPayExchangeRateGateway(ExchangeRateGateway):
    def __init__(
        self,
        cache: ExchangeRateCache,
        loader: CryptoPayRateLoader,
        clock: Clock,
        ttl: timedelta = timedelta(hours=6),
    ):
        self._cache: ExchangeRateCache = cache
        self._loader: CryptoPayRateLoader = loader
        self._clock: Clock = clock
        self._ttl: timedelta = ttl

    async def get(self, pair: CurrencyPair) -> ExchangeRate:
        rate = await self.get_many(pairs=[pair])
        return rate[0]

    async def get_many(
        self,
        pairs: Sequence[CurrencyPair],
    ) -> list[ExchangeRate]:
        cached: CachedExchangeRates | None = await self._cache.get()
        now = self._clock.now()
        if cached is not None and not cached.is_expired(
            ttl=self._ttl,
            now=now,
        ):
            return [self._get_or_raise(cached, pair) for pair in pairs]

        try:
            new_cached: CachedExchangeRates = await self._loader.load()
            await self._cache.set(new_cached)
            return [self._get_or_raise(new_cached, pair) for pair in pairs]
        except CodeErrorFactory as e:
            if cached is not None:
                logger.warning(
                    "An error occurred while retrieving new exchange rates, the old one is being used",  # noqa: E501
                )
                return [self._get_or_raise(cached, pair) for pair in pairs]
            raise ExchangeRateNotFound from e

    @staticmethod
    def _get_or_raise(
        cached: CachedExchangeRates,
        pair: CurrencyPair,
    ) -> ExchangeRate:
        try:
            return cached.rates[pair]
        except KeyError as e:
            raise ExchangeRateNotFound from e
