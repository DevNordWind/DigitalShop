import logging
from collections.abc import Sequence
from datetime import timedelta
from typing import override

from aiocryptopay.exceptions import (  # type: ignore[import-untyped]
    CodeErrorFactory,
)

from app.domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRate,
    ExchangeRateGateway,
    ExchangeRateNotFoundError,
)
from app.domain.common.port import Clock
from app.infra.common.rate_gateway.cache import ExchangeRateCache
from app.infra.common.rate_gateway.dto import CachedExchangeRates
from app.infra.common.rate_gateway.loader import CryptoPayRateLoader

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

    @override
    async def get(self, pair: CurrencyPair) -> ExchangeRate:
        rate = await self.get_many(pairs=[pair])
        return rate[0]

    @override
    async def get_many(
        self,
        pairs: Sequence[CurrencyPair],
    ) -> tuple[ExchangeRate, ...]:
        cached: CachedExchangeRates | None = await self._cache.get()
        now = self._clock.now()
        if cached is not None and not cached.is_expired(
            ttl=self._ttl,
            now=now,
        ):
            return tuple(self._get_or_raise(cached, pair) for pair in pairs)

        try:
            new_cached: CachedExchangeRates = await self._loader.load()
            await self._cache.set(new_cached)
            return tuple(self._get_or_raise(new_cached, pair) for pair in pairs)
        except CodeErrorFactory as e:
            if cached is not None:
                logger.warning(
                    "An error occurred while retrieving new exchange rates, the old one is being used",  # noqa: E501
                )
                return tuple(self._get_or_raise(cached, pair) for pair in pairs)
            raise ExchangeRateNotFoundError from e

    @staticmethod
    def _get_or_raise(
        cached: CachedExchangeRates,
        pair: CurrencyPair,
    ) -> ExchangeRate:
        try:
            return cached.rates[pair]
        except KeyError as e:
            raise ExchangeRateNotFoundError from e
