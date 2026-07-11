from abc import ABC, abstractmethod

from app.presentation.aiogram.setting.position.model import PositionSettings


class PositionSettingsGateway(ABC):
    @abstractmethod
    async def save(self, settings: PositionSettings) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> PositionSettings:
        raise NotImplementedError
