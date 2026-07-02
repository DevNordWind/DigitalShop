from collections.abc import Callable
from typing import Any, ClassVar, override

import orjson
from adaptix import Retort
from redis.asyncio import Redis

from app.presentation.aiogram.setting.position.exception import (
    PositionSettingsNotCreatedError,
)
from app.presentation.aiogram.setting.position.model import PositionSettings
from app.presentation.aiogram.setting.position.port import PositionSettingsGateway


class RedisPositionSettingsGateway(PositionSettingsGateway):
    KEY: ClassVar[str] = "bot:position_settings"

    def __init__(
        self,
        redis: Redis,
        retort: Retort,
        loads: Callable[[bytes | str], Any] = orjson.loads,
        dumps: Callable[[Any], str] = lambda obj: orjson.dumps(obj).decode(),
    ):
        self._redis: Redis = redis
        self._retort: Retort = retort
        self._loads: Callable[[bytes | str], Any] = loads
        self._dumps: Callable[[Any], str] = dumps

    @override
    async def save(self, settings: PositionSettings) -> None:
        dump = self._retort.dump(settings)

        await self._redis.set(name=self.KEY, value=self._dumps(dump))

    @override
    async def get(self) -> PositionSettings:
        raw_settings = await self._redis.get(name=self.KEY)

        if not raw_settings:
            raise PositionSettingsNotCreatedError

        loaded = self._loads(raw_settings)
        return self._retort.load(loaded, PositionSettings)
