from typing import ClassVar
from uuid import UUID

from adaptix import Retort
from redis.asyncio import Redis

from infra.presentation.aiogram.broadcast.dto import (
    BroadcastProgress,
    MessageResult,
)


class BroadcastProgressGateway:
    BROADCAST_ALIVE_TIME: int = 7200
    PREFIX: ClassVar[str] = "tg:broadcast:progress"

    def __init__(self, redis: Redis, retort: Retort):
        self._redis: Redis = redis
        self._retort: Retort = retort

    async def get(self, broadcast_id: UUID) -> BroadcastProgress | None:
        raw = await self._redis.hgetall(f"{self.PREFIX}:{broadcast_id}")  # type: ignore[misc]
        if not raw:
            return None

        return self._retort.load(raw, BroadcastProgress)

    async def set(self, progress: BroadcastProgress) -> None:
        key: str = f"{self.PREFIX}:{progress.id}"
        await self._redis.hset(  # type: ignore[misc]
            key, mapping=self._retort.dump(progress)
        )
        await self._redis.expire(key, self.BROADCAST_ALIVE_TIME)

    async def set_current_message_id(
        self, broadcast_id: UUID, message_id: int
    ) -> None:
        await self._redis.hset(  # type: ignore[misc]
            name=f"{self.PREFIX}:{broadcast_id}",
            key="current_message_id",
            value=str(message_id),
        )

    async def delete(self, broadcast_id: UUID) -> None:
        await self._redis.delete(f"{self.PREFIX}:{broadcast_id}")

    async def incr(self, broadcast_id: UUID, result: MessageResult) -> None:
        await self._redis.hincrby(  # type: ignore[misc]
            name=f"{self.PREFIX}:{broadcast_id}",
            key=result.value.lower(),
            amount=1,
        )
