import asyncio
from typing import ClassVar

from redis.asyncio import Redis


class BroadcastRateLimiter:
    KEY: ClassVar[str] = "tg:broadcast:limiter"

    def __init__(self, redis: Redis, limit_per_sec: int = 10):
        self._redis: Redis = redis
        self._limit_per_sec: int = limit_per_sec

    async def acquire(self) -> None:
        while True:
            async with self._redis.pipeline(transaction=True) as pipe:
                await pipe.incr(self.KEY)
                await pipe.expire(self.KEY, 1, nx=True)
                count, _ = await pipe.execute()

            if count < self._limit_per_sec:
                return

            ttl = await self._redis.ttl(self.KEY)
            await asyncio.sleep(ttl if ttl > 0 else 1)
