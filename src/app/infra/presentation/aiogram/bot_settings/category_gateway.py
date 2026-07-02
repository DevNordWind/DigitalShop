from collections.abc import Callable
from typing import Any, ClassVar, override

import orjson
from redis.asyncio import Redis

from app.domain.common.localized import Language
from app.presentation.aiogram.setting.category.exception import (
    CategorySettingsNotCreatedError,
)
from app.presentation.aiogram.setting.category.model import CategorySettings
from app.presentation.aiogram.setting.category.port import (
    CategorySettingsGateway,
)


class RedisCategorySettingsGateway(CategorySettingsGateway):
    KEY: ClassVar[str] = "bot:category_settings"

    def __init__(
        self,
        redis: Redis,
        loads: Callable[[bytes | str], Any] = orjson.loads,
        dumps: Callable[[Any], str] = lambda obj: orjson.dumps(obj).decode(),
    ):
        self._redis = redis
        self._loads = loads
        self._dumps = dumps

    @override
    async def save(self, settings: CategorySettings) -> None:
        dump: dict[str, Any] = {
            "default_lang": settings.default_lang,
            "show_with_no_items": settings.show_with_no_items,
        }

        await self._redis.set(name=self.KEY, value=self._dumps(dump))

    @override
    async def get(self) -> CategorySettings:
        raw_settings = await self._redis.get(name=self.KEY)

        if not raw_settings:
            raise CategorySettingsNotCreatedError

        loaded = self._loads(raw_settings)
        return CategorySettings(
            default_lang=Language(loaded["default_lang"]),
            show_with_no_items=loaded["show_with_no_items"],
        )
