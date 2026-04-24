from collections.abc import Callable
from typing import Any

import orjson
from adaptix import Retort
from domain.payment.enums import PaymentMethod
from presentation.aiogram.setting.payment.exception import (
    PaymentSettingsNotCreated,
)
from presentation.aiogram.setting.payment.model import PaymentSettings
from presentation.aiogram.setting.payment.port import (
    PaymentSettingsGateway,
)
from redis.asyncio import Redis


class PaymentSettingsGatewayImpl(PaymentSettingsGateway):
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
        self._prefix: str = f"bot:{bot_id}:payment_settings"

    async def save(self, settings: PaymentSettings) -> None:
        dump = self._retort.dump(settings)
        key = self._build_key(method=settings.method)

        await self._redis.set(key, self._dumps(dump))

    async def get(self) -> list[PaymentSettings]:
        keys = await self._redis.keys(f"{self._prefix}*")
        if not keys:
            raise PaymentSettingsNotCreated

        raw_settings = await self._redis.mget(keys)
        loaded_settings = [self._loads(raw) for raw in raw_settings]

        return [
            self._retort.load(loaded, PaymentSettings)
            for loaded in loaded_settings
        ]

    async def get_by_method(self, method: PaymentMethod) -> PaymentSettings:
        raw = await self._redis.get(self._build_key(method))
        if not raw:
            raise PaymentSettingsNotCreated
        loaded = self._loads(raw)

        return self._retort.load(loaded, PaymentSettings)

    def _build_key(self, method: PaymentMethod) -> str:
        return f"{self._prefix}:{method.value}"
