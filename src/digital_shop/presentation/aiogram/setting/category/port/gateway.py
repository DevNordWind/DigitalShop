from typing import Protocol

from presentation.aiogram.setting.category.model import CategorySettings


class CategorySettingsGateway(Protocol):
    async def save(self, settings: CategorySettings) -> None:
        raise NotImplementedError

    async def get(self) -> CategorySettings:
        raise NotImplementedError
