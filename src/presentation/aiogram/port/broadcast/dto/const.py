from typing import Final

from presentation.aiogram.port.broadcast.dto.button import DataButton
from presentation.aiogram.port.broadcast.dto.text import I18nText

DEFAULT_CLOSE_BUTTON: Final[DataButton] = DataButton(
    text=I18nText(key="inl-ui.close"), data="service:close"
)
