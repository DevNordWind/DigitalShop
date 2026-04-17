from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Url
from aiogram_dialog.widgets.text import Format

from presentation.aiogram.state import InfoState
from presentation.aiogram.widget import GetText

from .getter import info_getter

info = Window(
    GetText("user-info"),
    Url(
        text=GetText("user-info.support-btn"),
        url=Format("{support_url}"),
        when=F["support_exist"],
    ),
    Cancel(GetText("inl-ui.back")),
    state=InfoState.info,
    getter=info_getter,
)
