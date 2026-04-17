from collections.abc import Callable
from typing import Any

import orjson
from adaptix import Retort
from redis.asyncio import Redis

from presentation.aiogram.setting.category.exception import (
    CategorySettingsNotCreated,
)
from presentation.aiogram.setting.category.model import CategorySettings
from presentation.aiogram.setting.category.port import (
    CategorySettingsGateway,
)


class CategorySettingsGatewayImpl(CategorySettingsGateway):
    def __init__(
        self,
        redis: Redis,
        retort: Retort,
        bot_id: int,
        loads: Callable[[bytes | str], Any] = orjson.loads,
        dumps: Callable[[Any], str] = lambda obj: orjson.dumps(obj).decode(),
    ):
        self._redis: Redis = redis
        self._retort: Retort = retort
        self._bot_id: int = bot_id
        self._loads: Callable[[bytes | str], Any] = loads
        self._dumps: Callable[[Any], str] = dumps

    async def save(self, settings: CategorySettings) -> None:
        dump = self._retort.dump(settings)
        await self._redis.set(name=self._build_key(), value=self._dumps(dump))

    async def get(self) -> CategorySettings:
        key: str = self._build_key()
        raw_settings = await self._redis.get(name=key)

        if not raw_settings:
            raise CategorySettingsNotCreated

        loaded = self._loads(raw_settings)
        return self._retort.load(loaded, CategorySettings)

    def _build_key(
        self,
    ) -> str:
        return f"bot:{self._bot_id}:category_settings"
