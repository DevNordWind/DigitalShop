from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from domain.common.money import Currency
from presentation.aiogram.setting.position.cmd import (
    ChangePositionDefaultCurrency,
    ChangePositionDefaultCurrencyCmd,
    ChangePositionDefaultLang,
    ChangePositionDefaultLangCmd,
    SwitchShowPositionWithNoItems,
)


@inject
async def on_switch_with_no_items(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[SwitchShowPositionWithNoItems],
) -> None:
    return await handler()


@inject
async def on_change_default_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    new_lang: Language,
    handler: FromDishka[ChangePositionDefaultLang],
) -> None:
    return await handler(ChangePositionDefaultLangCmd(new_lang=new_lang))


@inject
async def on_change_default_currency(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    new_currency: Currency,
    handler: FromDishka[ChangePositionDefaultCurrency],
) -> None:
    return await handler(
        ChangePositionDefaultCurrencyCmd(new_currency=new_currency),
    )
