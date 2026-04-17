from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.query_params import SortingOrder
from app.product.category.cmd import (
    ArchiveAllCategories,
    ArchiveCategory,
    ArchiveCategoryCmd,
    DeleteAllCategories,
    DeleteCategory,
    DeleteCategoryCmd,
    RecoverCategory,
    RecoverCategoryCmd,
)
from domain.common.localized import Language
from domain.product.category.enums import CategoryStatus
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.admin.category.ctx import (
    CTX_KEY,
    AdminCategoryCtx,
)
from presentation.aiogram.state import (
    AdminCategoryState,
    EditCategoryState,
)


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
) -> None:
    if tg_ctx.lang is None:
        return

    ctx = AdminCategoryCtx(current_lang=tg_ctx.lang)

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_category(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    category_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    ctx.current_category_id = category_id
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    return await dialog_manager.switch_to(state=AdminCategoryState.category)


@inject
async def on_sorting_order(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    new_order = (
        SortingOrder.DESC
        if ctx.sorting_order == SortingOrder.ASC
        else SortingOrder.ASC
    )
    ctx.sorting_order = new_order

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_category_status(
    event: CallbackQuery,
    widget: Select[CategoryStatus],
    dialog_manager: DialogManager,
    status: CategoryStatus,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.status == status:
        ctx.status = None
    else:
        ctx.status = status

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.current_lang == lang:
        return

    ctx.current_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_edit_name(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    return await dialog_manager.start(
        state=EditCategoryState.edit_name,
        data={"category_id": ctx.current_category_id},
    )


@inject
async def on_edit_description(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    return await dialog_manager.start(
        state=EditCategoryState.edit_description,
        data={"category_id": ctx.current_category_id},
    )


@inject
async def on_edit_media(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    return await dialog_manager.start(
        state=EditCategoryState.edit_media,
        data={"category_id": ctx.current_category_id},
    )


@inject
async def on_archive_category(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[ArchiveCategory],
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.current_category_id is None:
        return

    await handler(ArchiveCategoryCmd(id=ctx.current_category_id))
    await dialog_manager.switch_to(state=AdminCategoryState.category)


@inject
async def on_recover_category(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[RecoverCategory],
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.current_category_id is None:
        return

    await handler(RecoverCategoryCmd(id=ctx.current_category_id))


@inject
async def on_delete_category(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[DeleteCategory],
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.current_category_id is None:
        return

    await handler(DeleteCategoryCmd(id=ctx.current_category_id))


@inject
async def on_delete_all_categories(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[DeleteAllCategories],
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.current_category_id is None:
        return

    await handler()


@inject
async def on_archive_all_categories(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[ArchiveAllCategories],
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.current_category_id is None:
        return

    await handler()
