from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Select
from app.product.position.cmd import (
    AddPositionItem,
    AddPositionItemCmd,
    ArchivePositionItem,
    ArchivePositionItemCmd,
    DeletePositionItem,
    DeletePositionItemCmd,
    RecoverPositionItem,
    RecoverPositionItemCmd,
    ReplacePositionItem,
    ReplacePositionItemCmd,
)
from app.product.position.dto.item_content import ItemRawDTO
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from presentation.aiogram.dialog.admin.position.fixed_item.ctx import (
    CTX_KEY,
    PositionFixedItemCtx,
)
from presentation.aiogram.state import FixedItemState


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = PositionFixedItemCtx(
        position_id=dialog_manager.start_data["position_id"],  # type: ignore[index, call-overload,arg-type]
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_replace_item_text(
    event: Message,
    widget: TextInput[str],
    dialog_manager: DialogManager,
    item_content: str,
    handler: FromDishka[ReplacePositionItem],
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionFixedItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )
    if ctx.current_item_id is None:
        return

    await handler(
        ReplacePositionItemCmd(
            item_id=ctx.current_item_id,
            new_item_raw=ItemRawDTO(value=item_content),
        ),
    )

    await event.delete()
    await dialog_manager.switch_to(
        state=FixedItemState.item,
        show_mode=ShowMode.EDIT,
    )


@inject
async def on_add_item_text(
    event: Message,
    widget: TextInput[str],
    dialog_manager: DialogManager,
    item_content: str,
    handler: FromDishka[AddPositionItem],
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionFixedItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )

    await handler(
        AddPositionItemCmd(
            id=ctx.position_id,
            item_raw=ItemRawDTO(value=item_content),
        ),
    )

    await event.delete()
    await dialog_manager.switch_to(
        state=FixedItemState.item,
        show_mode=ShowMode.EDIT,
    )


@inject
async def on_archive_item(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[ArchivePositionItem],
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionFixedItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )
    if ctx.current_item_id is None:
        return

    await handler(ArchivePositionItemCmd(item_id=ctx.current_item_id))


@inject
async def on_delete_archived_item(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[DeletePositionItem],
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionFixedItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )
    if ctx.current_archived_item_id is None:
        return

    await handler(DeletePositionItemCmd(item_id=ctx.current_archived_item_id))


@inject
async def on_select_archived_item(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    archived_item_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionFixedItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )
    ctx.current_archived_item_id = archived_item_id

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(state=FixedItemState.archived_item)


@inject
async def on_recover_archived_item(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[RecoverPositionItem],
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionFixedItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )
    if ctx.current_archived_item_id is None:
        return

    await handler(RecoverPositionItemCmd(item_id=ctx.current_archived_item_id))
