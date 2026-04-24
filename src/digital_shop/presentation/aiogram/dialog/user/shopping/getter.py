from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from app.common.dto.file_key.mapper import (
    FileKeyMapper as ApplicationFileKeyMapper,
)
from app.common.dto.money import MoneyDTO
from app.common.dto.query_params import OffsetPaginationParams, SortingOrder
from app.product.category.dto.category import CategoryDTO
from app.product.category.dto.paginated import CategoriesShortPaginated
from app.product.category.dto.sorting import CategorySortingParams
from app.product.category.query import (
    GetCategory,
    GetCategoryQuery,
    ListShortCategories,
    ListShortCategoriesQuery,
)
from app.product.position.dto.paginated import (
    PositionWithItemsAmountPaginated,
)
from app.product.position.dto.position import (
    PositionDTO,
    PositionWithItemsAmount,
)
from app.product.position.dto.sorting import PositionSortingParams
from app.product.position.query import (
    GetPositionWithItemsAmount,
    GetPositionWithItemsAmountQuery,
    ListPositionsWithItemsAmountByCategory,
    ListPositionsWithItemsAmountByCategoryQuery,
)
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.file import FileKey
from domain.common.money import Currency
from domain.product.category.enums import CategoryStatus
from domain.product.position.enums import PositionStatus, WarehouseType
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.user.shopping.ctx import (
    CATEGORIES_HEIGHT,
    CATEGORIES_SCROLL,
    CTX_KEY,
    POSITION_MEDIA_SCROLL,
    POSITIONS_HEIGHT,
    POSITIONS_SCROLL,
    ShoppingCtx,
)
from presentation.aiogram.mapper import FileKeyMapper
from presentation.aiogram.setting.category.model import CategorySettings
from presentation.aiogram.setting.position.model import PositionSettings


@dataclass(slots=True, frozen=True)
class CategoryButton:
    id: UUID

    name: str


@dataclass(slots=True, frozen=True)
class PositionButton:
    id: UUID

    name: str

    items_amount: int
    type: WarehouseType

    amount: Decimal
    currency: Currency


@inject
async def select_category_getter(
    dialog_manager: DialogManager,
    settings: FromDishka[CategorySettings],
    query_handler: FromDishka[ListShortCategories],
    ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    current_page: int = await dialog_manager.find(CATEGORIES_SCROLL).get_page()  # type: ignore[union-attr]
    offset: int = current_page * CATEGORIES_HEIGHT

    paginated: CategoriesShortPaginated = await query_handler(
        ListShortCategoriesQuery(
            pagination=OffsetPaginationParams(
                limit=CATEGORIES_HEIGHT,
                offset=offset,
            ),
            sorting=CategorySortingParams(
                field="created_at",
                order=SortingOrder.DESC,
            ),
            status=CategoryStatus.AVAILABLE,
            show_with_no_items=settings.show_with_no_items,
        ),
    )

    return {
        "pages": (paginated.total + CATEGORIES_HEIGHT - 1)
        // CATEGORIES_HEIGHT,
        "buttons": [
            CategoryButton(
                id=category.id,
                name=category.name.get_with_fallback(ctx.lang),
            )
            for category in paginated.categories
        ],
        "has_categories": bool(paginated.categories),
    }


@inject
async def select_position_getter(
    dialog_manager: DialogManager,
    settings: FromDishka[PositionSettings],
    positions_handler: FromDishka[ListPositionsWithItemsAmountByCategory],
    category_handler: FromDishka[GetCategory],
    tg_ctx: FromDishka[TelegramContextDTO],
    mapper: FromDishka[FileKeyMapper],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: ShoppingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ShoppingCtx,
    )
    if ctx.current_category_id is None:
        return {}

    current_page: int = await dialog_manager.find(POSITIONS_SCROLL).get_page()  # type: ignore[union-attr]
    offset: int = current_page * POSITIONS_HEIGHT

    category: CategoryDTO = await category_handler(
        GetCategoryQuery(id=ctx.current_category_id),
    )
    media: MediaAttachment | None = None
    if category.media is not None:
        key: FileKey = ApplicationFileKeyMapper.to_value_object(
            src=category.media,
        )
        media = await mapper.to_media_attachment(key=key)

    paginated: PositionWithItemsAmountPaginated = await positions_handler(
        ListPositionsWithItemsAmountByCategoryQuery(
            pagination=OffsetPaginationParams(
                limit=POSITIONS_HEIGHT,
                offset=offset,
            ),
            sorting=PositionSortingParams(
                field="created_at",
                order=SortingOrder.DESC,
            ),
            show_with_no_items=settings.show_with_no_items,
            category_id=category.id,
            status=PositionStatus.AVAILABLE,
        ),
    )
    buttons: list[PositionButton] = []

    for position_with_items in paginated.positions:
        money = position_with_items.position.price.get(
            currency=tg_ctx.currency
        )
        buttons.append(
            PositionButton(
                id=position_with_items.position.id,
                name=position_with_items.position.name.get_with_fallback(
                    lang=tg_ctx.lang
                ),
                amount=money.amount,
                currency=money.currency,
                items_amount=position_with_items.items_amount,
                type=position_with_items.position.warehouse_type,
            ),
        )

    return {
        "pages": (paginated.total + POSITIONS_HEIGHT - 1) // POSITIONS_HEIGHT,
        "buttons": buttons,
        "category_name": category.name.get_with_fallback(tg_ctx.lang),
        "category_description": category.description.get_with_fallback(
            tg_ctx.lang,
        )
        if category.description
        else None,
        "media": media,
    }


@inject
async def position_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetPositionWithItemsAmount],
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
    mapper: FromDishka[FileKeyMapper],
    **_: Any,
) -> dict[str, Any] | None:
    ctx: ShoppingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ShoppingCtx,
    )
    current_page: int = await dialog_manager.find(  # type: ignore[union-attr]
        POSITION_MEDIA_SCROLL,
    ).get_page()
    if ctx.current_position_id is None:
        return None

    position_with_items: PositionWithItemsAmount = await query_handler(
        GetPositionWithItemsAmountQuery(id=ctx.current_position_id),
    )
    position: PositionDTO = position_with_items.position

    media: MediaAttachment | None = None
    money: MoneyDTO = position.price.get(currency=tg_ctx.currency)

    if position.media:
        media = await mapper.to_media_attachment(
            key=ApplicationFileKeyMapper.to_value_object(
                src=position.media[current_page],
            ),
        )

    ctx.current_position_warehouse_type = position.warehouse_type
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    return {
        "name": position.name.get_with_fallback(lang=tg_ctx.lang),
        "description": position.description.get_with_fallback(lang=tg_ctx.lang)
        if position.description
        else None,
        "media": media,
        "pages": len(position.media),
        "amount": money.amount,
        "currency": money.currency,
        "items_amount": position_with_items.items_amount,
        "type": position.warehouse_type,
    }


@inject
async def input_items_amount_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetPositionWithItemsAmount],
    **_: Any,
) -> dict[str, Any]:
    ctx: ShoppingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ShoppingCtx,
    )
    if ctx.current_position_id is None:
        return {}

    position: PositionWithItemsAmount = await query_handler(
        GetPositionWithItemsAmountQuery(id=ctx.current_position_id),
    )

    return {"count": position.items_amount}
