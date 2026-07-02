from typing import Final

from app.presentation.aiogram.port.broadcast.dto.button import DataButton
from app.presentation.aiogram.port.broadcast.dto.text import I18nText

DEFAULT_CLOSE_BUTTON: Final[DataButton] = DataButton(
    text=I18nText(key="inl-ui.close"), data="service:close"
)
