import asyncio
from dataclasses import fields
from datetime import datetime
from typing import Any, override

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text as DialogText
from dishka import AsyncContainer
from dishka.integrations.aiogram_dialog import CONTAINER_NAME

from app.presentation.aiogram.port.text import Text
from app.presentation.aiogram.util.timezone_processor import TimeZoneProcessor


class GetTextGetterKey(DialogText):
    def __init__(self, getter_key: str, when: WhenCondition | None = None):
        super().__init__(when)
        self.getter_key: str = getter_key

    @override
    async def _render_text(self, data: dict[str, Any], manager: DialogManager) -> str:
        container: AsyncContainer = manager.middleware_data[CONTAINER_NAME]

        text, time_zone = await asyncio.gather(
            container.get(Text),
            container.get(TimeZoneProcessor),
        )
        localized_data: dict[str, Any] = {
            k: time_zone.process(v) if isinstance(v, datetime) else v
            for k, v in data.items()
        }

        return text(data[self.getter_key], **localized_data)


class GetText(DialogText):
    """This class produced by Text"""

    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when)
        self.key = key

    @override
    async def _render_text(self, data: dict[str, Any], manager: DialogManager) -> str:
        container: AsyncContainer = manager.middleware_data[CONTAINER_NAME]

        text, time_zone = await asyncio.gather(
            container.get(Text),
            container.get(TimeZoneProcessor),
        )
        localized_data: dict[str, Any] = {
            k: time_zone.process(v) if isinstance(v, datetime) else v
            for k, v in data.items()
        }

        return text(self.key, **localized_data)


class GetTextSelect(DialogText):
    """This class produced by Text"""

    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when)
        self.key = key

    @override
    async def _render_text(self, data: dict[str, Any], manager: DialogManager) -> str:
        container: AsyncContainer = manager.middleware_data[CONTAINER_NAME]

        text, time_zone = await asyncio.gather(
            container.get(Text),
            container.get(TimeZoneProcessor),
        )
        localized_data: dict[str, Any] = {}
        for field in fields(data["item"]):
            value: object = getattr(data["item"], field.name)
            if isinstance(value, datetime):
                localized_data[field.name] = time_zone.process(dt=value)
            else:
                localized_data[field.name] = value

        return text(
            self.key,
            **localized_data,
        )
