from abc import ABC, abstractmethod

from app.presentation.aiogram.setting.category.model import CategorySettings


class CategorySettingsGateway(ABC):
    @abstractmethod
    async def save(self, settings: CategorySettings) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> CategorySettings:
        raise NotImplementedError
