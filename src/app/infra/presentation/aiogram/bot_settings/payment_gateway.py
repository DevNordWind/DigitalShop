from collections.abc import Callable
from typing import Any, ClassVar, override

import orjson
from adaptix import Retort
from redis.asyncio import Redis

from app.domain.payment.enums import PaymentMethod
from app.presentation.aiogram.setting.payment.exception import (
    PaymentSettingsNotCreatedError,
)
from app.presentation.aiogram.setting.payment.model import PaymentSettings
from app.presentation.aiogram.setting.payment.port import (
    PaymentSettingsGateway,
)


class RedisPaymentSettingsGateway(PaymentSettingsGateway):
    PREFIX: ClassVar[str] = "bot:payment_settings"

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
    async def save(self, settings: PaymentSettings) -> None:
        dump: dict[str, Any] = self._retort.dump(settings)
        key: str = self._build_key(method=settings.method)

        await self._redis.set(key, self._dumps(dump))

    @override
    async def get(self) -> list[PaymentSettings]:
        keys = await self._redis.keys(f"{self.PREFIX}:*")

        if not keys:
            raise PaymentSettingsNotCreatedError

        raw_settings = await self._redis.mget(keys)
        loaded_settings = [self._loads(raw) for raw in raw_settings]  # type: ignore[bad-argument-type]

        return self._retort.load(loaded_settings, list[PaymentSettings])

    @override
    async def get_by_method(self, method: PaymentMethod) -> PaymentSettings:
        raw = await self._redis.get(self._build_key(method))
        if not raw:
            raise PaymentSettingsNotCreatedError

        loaded = self._loads(raw)

        return self._retort.load(loaded, PaymentSettings)

    def _build_key(self, method: PaymentMethod) -> str:
        return f"{self.PREFIX}:{method.value}"
