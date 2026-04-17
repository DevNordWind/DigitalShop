from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import (
    ManagedTextInput,
    TextInput,
)
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.query_params import SortingOrder
from app.product.position.cmd import (
    AddPositionItems,
    AddPositionItemsCmd,
    ArchiveAllPositionItems,
    ArchiveAllPositionItemsCmd,
    ArchivePositionItem,
    ArchivePositionItemCmd,
    DeleteAllPositionItems,
    DeleteAllPositionItemsCmd,
    DeletePositionItem,
    DeletePositionItemCmd,
    RecoverPositionItem,
    RecoverPositionItemCmd,
    ReplacePositionItem,
    ReplacePositionItemCmd,
)
from app.product.position.dto.item_content import ItemRawDTO
from domain.product.position.item.enums import ItemStatus
from presentation.aiogram.dialog.admin.position.fixed_item.ctx import (
    PositionFixedItemCtx,
)
from presentation.aiogram.dialog.admin.position.stock_item.ctx import (
    CTX_KEY,
    ItemsFilters,
    PositionStockItemCtx,
)
from presentation.aiogram.port import Text
from presentation.aiogram.state import StockItemState


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = PositionStockItemCtx(
        position_id=data["position_id"],
        filters=ItemsFilters(
            order=SortingOrder.DESC,
            status=ItemStatus.AVAILABLE,
        ),
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_filter_order(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    ctx.filters.order = (
        SortingOrder.DESC
        if ctx.filters.order == SortingOrder.ASC
        else SortingOrder.ASC
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_item_status(
    event: CallbackQuery,
    widget: Select[ItemStatus],
    dialog_manager: DialogManager,
    status: ItemStatus,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    if ctx.filters.status == status:
        ctx.filters.status = None
    else:
        ctx.filters.status = status

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_item(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    item_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    ctx.current_item_id = item_id
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(state=StockItemState.item)


@inject
async def on_add_item_text(
    event: Message,
    widget: TextInput[str],
    dialog_manager: DialogManager,
    item_content: str,
    handler: FromDishka[AddPositionItems],
    retort: FromDishka[Retort],
    t: FromDishka[Text],
) -> None:
    ctx: PositionFixedItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )

    items: list[str] = item_content.split("\n\n")

    items_ids = await handler(
        AddPositionItemsCmd(
            id=ctx.position_id,
            items_raw=[ItemRawDTO(value=item) for item in items],
        ),
    )
    await event.reply(
        text=t(
            "admin-position-warehouse-add-stock.success",
            count=len(items_ids),
        ),
    )

    await dialog_manager.switch_to(
        state=StockItemState.items,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


@inject
async def on_archive_item(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[ArchivePositionItem],
) -> None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    if ctx.current_item_id is None:
        return

    await handler(ArchivePositionItemCmd(item_id=ctx.current_item_id))


@inject
async def on_delete_item(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[DeletePositionItem],
) -> None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    if ctx.current_item_id is None:
        return

    await handler(DeletePositionItemCmd(item_id=ctx.current_item_id))


@inject
async def on_recover_item(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[RecoverPositionItem],
) -> None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    if ctx.current_item_id is None:
        return

    await handler(RecoverPositionItemCmd(item_id=ctx.current_item_id))


@inject
async def on_archive_all(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[ArchiveAllPositionItems],
) -> None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    await handler(ArchiveAllPositionItemsCmd(position_id=ctx.position_id))


@inject
async def on_delete_all(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[DeleteAllPositionItems],
) -> None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    await handler(DeleteAllPositionItemsCmd(position_id=ctx.position_id))


@inject
async def on_replace_item_content_text(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    new_content: str,
    retort: FromDishka[Retort],
    handler: FromDishka[ReplacePositionItem],
) -> None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    if ctx.current_item_id is None:
        return

    await handler(
        ReplacePositionItemCmd(
            item_id=ctx.current_item_id,
            new_item_raw=ItemRawDTO(value=new_content),
        ),
    )
    dialog_manager.show_mode = ShowMode.EDIT
    await event.delete()
    await dialog_manager.switch_to(
        state=StockItemState.item,
        show_mode=ShowMode.EDIT,
    )
