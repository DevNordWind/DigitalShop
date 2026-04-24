from typing import Protocol

from presentation.aiogram.setting.general.model import GeneralBotSettings


class GeneralBotSettingsGateway(Protocol):
    async def save(self, settings: GeneralBotSettings) -> None:
        raise NotImplementedError

    async def get(self) -> GeneralBotSettings:
        raise NotImplementedError
