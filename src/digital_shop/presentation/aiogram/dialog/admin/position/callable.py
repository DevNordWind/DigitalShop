from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import Button, Select
from app.common.dto.query_params import SortingOrder
from app.product.position.cmd import (
    ArchiveAllPositionsInCategory,
    ArchiveAllPositionsInCategoryCmd,
    ArchivePosition,
    ArchivePositionCmd,
    DeleteAllPositionsInCategory,
    DeleteAllPositionsInCategoryCmd,
    DeletePosition,
    DeletePositionCmd,
    RecoverPosition,
    RecoverPositionCmd,
)
from app.product.position.dto.position import PositionDTO
from app.product.position.query import GetPosition, GetPositionQuery
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from domain.product.category.enums import CategoryStatus
from domain.product.position.enums import PositionStatus
from domain.product.position.enums.warehouse import WarehouseType
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.admin.position.ctx import (
    CTX_KEY,
    POSITION_MEDIA_SCROLL,
    AdminPositionCtx,
)
from presentation.aiogram.state import (
    AdminPositionState,
    CreatePositionState,
    EditPositionState,
    FixedItemState,
    StockItemState,
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

    ctx = AdminPositionCtx(current_lang=tg_ctx.lang)
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_category_sorting_order(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    new_order = (
        SortingOrder.DESC
        if ctx.category_sorting_order == SortingOrder.ASC
        else SortingOrder.ASC
    )
    ctx.category_sorting_order = new_order

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_category_status(
    event: CallbackQuery,
    widget: Select[CategoryStatus],
    dialog_manager: DialogManager,
    category_status: CategoryStatus,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if category_status == ctx.category_status:
        ctx.category_status = None
    else:
        ctx.category_status = category_status

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_position_sorting_order(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    new_order = (
        SortingOrder.DESC
        if ctx.position_sorting_order == SortingOrder.ASC
        else SortingOrder.ASC
    )
    ctx.position_sorting_order = new_order

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_position_status(
    event: CallbackQuery,
    widget: Select[PositionStatus],
    dialog_manager: DialogManager,
    position_status: PositionStatus,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if position_status == ctx.position_status:
        ctx.position_status = None
    else:
        ctx.position_status = position_status

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_category(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    category_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    ctx.current_category_id = category_id

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(state=AdminPositionState.select_position)


@inject
async def on_select_position(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    position_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    ctx.current_position_id = position_id

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(state=AdminPositionState.position)


@inject
async def on_create(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )

    await dialog_manager.start(
        state=CreatePositionState.view,
        data={"category_id": ctx.current_category_id},
    )


@inject
async def on_select_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    ctx.current_lang = lang

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


async def on_position_back(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    scroll_widget: ManagedScroll = dialog_manager.find(POSITION_MEDIA_SCROLL)  # type: ignore[assignment]
    await scroll_widget.set_page(0)


@inject
async def on_edit_name(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )

    await dialog_manager.start(
        state=EditPositionState.edit_name,
        data={"position_id": ctx.current_position_id},
    )


@inject
async def on_edit_description(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )

    await dialog_manager.start(
        state=EditPositionState.edit_description,
        data={"position_id": ctx.current_position_id},
    )


@inject
async def on_edit_price(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )

    await dialog_manager.start(
        state=EditPositionState.edit_price,
        data={"position_id": ctx.current_position_id},
    )


@inject
async def on_edit_media(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )

    await dialog_manager.start(
        state=EditPositionState.edit_media,
        data={"position_id": ctx.current_position_id},
    )


@inject
async def on_edit_item(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[GetPosition],
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_position_id is None:
        return None

    position: PositionDTO = await handler(
        GetPositionQuery(id=ctx.current_position_id),
    )

    if position.warehouse_type == WarehouseType.FIXED:
        return await dialog_manager.start(
            state=FixedItemState.item,
            data={"position_id": position.id},
        )

    return await dialog_manager.start(
        state=StockItemState.items,
        data={"position_id": position.id},
    )


@inject
async def on_archive_position(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[ArchivePosition],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_position_id is None:
        return

    await handler(ArchivePositionCmd(id=ctx.current_position_id))
    await dialog_manager.switch_to(state=AdminPositionState.position)


@inject
async def on_delete_position(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[DeletePosition],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_position_id is None:
        return

    await handler(DeletePositionCmd(id=ctx.current_position_id))

    await dialog_manager.switch_to(state=AdminPositionState.select_position)


@inject
async def on_archive_all_positions(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[ArchiveAllPositionsInCategory],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_category_id is None:
        return

    await handler(
        ArchiveAllPositionsInCategoryCmd(category_id=ctx.current_category_id),
    )


@inject
async def on_delete_all_positions(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[DeleteAllPositionsInCategory],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_category_id is None:
        return

    await handler(
        DeleteAllPositionsInCategoryCmd(category_id=ctx.current_category_id),
    )


@inject
async def on_recover_position(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[RecoverPosition],
) -> None:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_position_id is None:
        return

    await handler(RecoverPositionCmd(id=ctx.current_position_id))
