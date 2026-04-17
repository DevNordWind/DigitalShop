from collections.abc import Callable
from typing import Any

import orjson
from adaptix import Retort
from redis.asyncio import Redis

from presentation.aiogram.setting.general.exception import (
    GeneralSettingsNotCreated,
)
from presentation.aiogram.setting.general.model import GeneralBotSettings
from presentation.aiogram.setting.general.port import (
    GeneralBotSettingsGateway,
)


class GeneralBotSettingsGatewayImpl(GeneralBotSettingsGateway):
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

    async def save(self, settings: GeneralBotSettings) -> None:
        dump = self._retort.dump(settings)

        await self._redis.set(name=self._build_key(), value=self._dumps(dump))

    async def get(self) -> GeneralBotSettings:
        key: str = self._build_key()
        raw_settings = await self._redis.get(name=key)

        if not raw_settings:
            raise GeneralSettingsNotCreated

        loaded = self._loads(raw_settings)
        return self._retort.load(loaded, GeneralBotSettings)

    def _build_key(
        self,
    ) -> str:
        return f"bot:{self._bot_id}:general_settings"
