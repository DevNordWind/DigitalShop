from typing import Protocol

from presentation.aiogram.setting.position.model import PositionSettings


class PositionSettingsGateway(Protocol):
    async def save(self, settings: PositionSettings) -> None:
        raise NotImplementedError

    async def get(self) -> PositionSettings:
        raise NotImplementedError
