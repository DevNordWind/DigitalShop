from collections.abc import Callable
from typing import Any

import orjson
from adaptix import Retort
from redis.asyncio import Redis

from infra.common.rate_gateway.dto import CachedExchangeRates


class ExchangeRateCache:
    CACHE_KEY = "exchange_rates:cryptobot:v1"

    def __init__(
        self,
        redis: Redis,
        retort: Retort,
        loads: Callable[[bytes | str], Any] = orjson.loads,
        dumps: Callable[[Any], str] = lambda obj: orjson.dumps(obj).decode(),
    ) -> None:
        self._redis = redis
        self._retort = retort
        self._loads = loads
        self._dumps = dumps

    async def get(self) -> CachedExchangeRates | None:
        raw = await self._redis.get(self.CACHE_KEY)
        if not raw:
            return None

        return self._retort.load(self._loads(raw), CachedExchangeRates)

    async def set(self, cached: CachedExchangeRates) -> None:
        dump = self._retort.dump(cached)
        await self._redis.set(self.CACHE_KEY, self._dumps(dump))
