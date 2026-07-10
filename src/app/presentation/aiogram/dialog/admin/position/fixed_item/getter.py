from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.app.common.dto.query_params import OffsetPaginationParams, SortingOrder
from app.app.shopping.position.dto.item import ItemDTO
from app.app.shopping.position.dto.paginated import PositionItemsPaginated
from app.app.shopping.position.query import (
    GetPositionItem,
    GetPositionItemQuery,
    ListPositionItems,
    ListPositionItemsQuery,
)
from app.domain.shopping.position.enums import WarehouseType
from app.domain.shopping.position.item.enums import FixedItemStatus
from app.presentation.aiogram.dialog.admin.position.fixed_item.ctx import (
    ARCHIVED_ITEMS_SCROLL_HEIGHT,
    ARCHIVED_ITEMS_SCROLL_ID,
    CTX_KEY,
    PositionFixedItemCtx,
)


@dataclass(slots=True, frozen=True)
class ItemButton:
    id: UUID

    item_value: str

    created_at: datetime
    archived_at: datetime | None


@inject
async def item_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[ListPositionItems],
    **_: Any,
) -> dict[str, Any]:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )
    paginated: PositionItemsPaginated = await query_handler(
        query=ListPositionItemsQuery(
            id=ctx.position_id,
            sorting_order=SortingOrder.DESC,
            pagination=OffsetPaginationParams(limit=1, offset=0),
            status=FixedItemStatus.AVAILABLE,
        ),
    )
    item: ItemDTO | None = None
    if paginated.items:
        item = paginated.items[0]

    if item is None:
        return {"has_item": False, "type": WarehouseType.FIXED}

    ctx.current_item_id = item.id
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    return {
        "has_item": True,
        "type": WarehouseType.FIXED,
        "item_value": item.content.value,
        "created_at": item.created_at,
        "is_archived": item.status == FixedItemStatus.ARCHIVED,
    }


@inject
async def archive_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[ListPositionItems],
    **_: Any,
) -> dict[str, Any]:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )
    current_page: int = await dialog_manager.find(  # type: ignore[union-attr]
        widget_id=ARCHIVED_ITEMS_SCROLL_ID,
    ).get_page()
    offset: int = current_page * ARCHIVED_ITEMS_SCROLL_HEIGHT

    paginated: PositionItemsPaginated = await query_handler(
        ListPositionItemsQuery(
            id=ctx.position_id,
            sorting_order=SortingOrder.DESC,
            pagination=OffsetPaginationParams(
                limit=ARCHIVED_ITEMS_SCROLL_HEIGHT,
                offset=offset,
            ),
            status=FixedItemStatus.ARCHIVED,
        ),
    )

    return {
        "buttons": [
            ItemButton(
                id=item.id,
                item_value=item.content.value[:12],
                created_at=item.created_at,
                archived_at=item.archived_at,
            )
            for item in paginated.items
        ],
        "pages": (paginated.total + ARCHIVED_ITEMS_SCROLL_HEIGHT - 1)
        // ARCHIVED_ITEMS_SCROLL_HEIGHT,
    }


@inject
async def archived_item_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetPositionItem],
    **_: Any,
) -> dict[str, Any]:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionFixedItemCtx,
    )
    if ctx.current_archived_item_id is None:
        return {}

    item: ItemDTO = await query_handler(
        GetPositionItemQuery(item_id=ctx.current_archived_item_id),
    )

    return {
        "item_value": item.content.value,
        "created_at": item.created_at,
        "archived_at": item.archived_at,
    }
