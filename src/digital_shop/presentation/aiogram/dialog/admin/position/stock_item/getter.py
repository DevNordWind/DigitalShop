from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram_dialog import DialogManager
from app.common.dto.query_params import OffsetPaginationParams
from app.product.position.dto.item import FiniteItemDTO, ItemDTO
from app.product.position.dto.paginated import PositionItemsPaginated
from app.product.position.dto.sorting import PositionItemsSortingParams
from app.product.position.query import (
    GetPositionItem,
    GetPositionItemQuery,
    ListPositionItems,
    ListPositionItemsQuery,
)
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.product.position.enums import WarehouseType
from domain.product.position.item.enums import (
    ItemContentType,
    ItemStatus,
)
from presentation.aiogram.dialog.admin.position.stock_item.ctx import (
    CTX_KEY,
    ITEMS_HEIGHT,
    ITEMS_SCROLL,
    PositionStockItemCtx,
)


@dataclass(slots=True, frozen=True)
class ItemButton:
    id: UUID

    item_type: ItemContentType
    item_value: str

    created_at: datetime


@dataclass(slots=True, frozen=True)
class ItemStatusButton:
    item_status: ItemStatus

    is_current: bool


@inject
async def items_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[ListPositionItems],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    current_page: int = await dialog_manager.find(ITEMS_SCROLL).get_page()  # type: ignore[union-attr]
    offset: int = current_page * ITEMS_HEIGHT

    paginated: PositionItemsPaginated = await query_handler(
        ListPositionItemsQuery(
            id=ctx.position_id,
            sorting=PositionItemsSortingParams(
                field="created_at",
                order=ctx.filters.order,
            ),
            pagination=OffsetPaginationParams(
                limit=ITEMS_HEIGHT,
                offset=offset,
            ),
            status=ctx.filters.status,
        ),
    )

    return {
        "pages": (paginated.total + ITEMS_HEIGHT - 1) // ITEMS_HEIGHT,
        "buttons": [
            ItemButton(
                id=item.id,
                item_type=item.content.type,
                item_value=item.content.value[:12],
                created_at=item.created_at,
            )
            for item in paginated.items
        ],
        "type": WarehouseType.STOCK,
    }


@inject
async def item_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetPositionItem],
    **_: Any,
) -> dict[str, Any] | None:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )
    if ctx.current_item_id is None:
        return {}

    item: ItemDTO = await query_handler(
        GetPositionItemQuery(id=ctx.current_item_id),
    )
    if not isinstance(item, FiniteItemDTO):
        return {}

    return {
        "item_type": item.content.type,
        "item_value": item.content.value,
        "item_status": item.status,
        "created_at": item.created_at,
        "sold_at": item.sold_at,
        "archived_at": item.archived_at,
        "reserved_at": item.reserved_at,
    }


@inject
async def filters_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionStockItemCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionStockItemCtx,
    )

    return {
        "buttons": [
            ItemStatusButton(
                item_status=status,
                is_current=status == ctx.filters.status,
            )
            for status in ItemStatus
        ],
        "sorting_order": ctx.filters.order,
    }
