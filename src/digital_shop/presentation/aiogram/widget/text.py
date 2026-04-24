from dataclasses import fields

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text as DialogText
from dishka.integrations.aiogram_dialog import CONTAINER_NAME
from presentation.aiogram.port.text import Text


class GetTextGetterKey(DialogText):
    def __init__(self, getter_key: str, when: WhenCondition | None = None):
        super().__init__(when)
        self.getter_key: str = getter_key

    async def _render_text(self, data, manager: DialogManager) -> str:  # type: ignore[no-untyped-def]
        text: Text = await manager.middleware_data[CONTAINER_NAME].get(Text)
        return text(data[self.getter_key], **data)


class GetText(DialogText):
    """This class produced by Text"""

    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when)
        self.key = key

    async def _render_text(self, data, manager: DialogManager) -> str:  # type: ignore[no-untyped-def]
        text: Text = await manager.middleware_data[CONTAINER_NAME].get(Text)
        return text(self.key, **data)


class GetTextSelect(DialogText):
    """This class produced by Text"""

    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when)
        self.key = key

    async def _render_text(self, data, manager: DialogManager) -> str:  # type: ignore[no-untyped-def]
        text: Text = await manager.middleware_data[CONTAINER_NAME].get(Text)
        item = data["item"]

        return text(
            self.key,
            **{f.name: getattr(item, f.name) for f in fields(item)},
        )
