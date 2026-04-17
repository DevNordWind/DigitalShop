from uuid import UUID

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.query_params import SortingOrder
from domain.common.localized import Language
from presentation.aiogram.setting.category.cmd import (
    ChangeCategoryDefaultLang,
    ChangeCategoryDefaultLangCmd,
    SwitchWithNoItemsCategory,
)
from presentation.aiogram.state import (
    AdminCategoryState,
)


async def on_select_category(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    category_id: UUID,
) -> None:
    dialog_manager.dialog_data["category_id"] = category_id

    return await dialog_manager.switch_to(state=AdminCategoryState.category)


async def on_order(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    order: SortingOrder = dialog_manager.dialog_data.get(
        "sorting_order",
        SortingOrder.DESC,
    )
    dialog_manager.dialog_data["sorting_order"] = (
        SortingOrder.DESC if order == SortingOrder.ASC else SortingOrder.ASC
    )


async def on_select_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
) -> None:
    dialog_manager.dialog_data["current_lang"] = lang


@inject
async def on_switch_with_no_items(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[SwitchWithNoItemsCategory],
) -> None:
    return await handler()


@inject
async def on_change_default_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    handler: FromDishka[ChangeCategoryDefaultLang],
) -> None:
    return await handler(ChangeCategoryDefaultLangCmd(new_lang=lang))
