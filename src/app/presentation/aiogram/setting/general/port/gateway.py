from abc import ABC, abstractmethod

from app.presentation.aiogram.setting.general.model import GeneralBotSettings


class GeneralBotSettingsGateway(ABC):
    @abstractmethod
    async def save(self, settings: GeneralBotSettings) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> GeneralBotSettings:
        raise NotImplementedError
