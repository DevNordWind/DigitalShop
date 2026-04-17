from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.file_key import FileKeyMapper as AppFileKeyMapper
from app.common.dto.query_params import (
    OffsetPaginationParams,
)
from app.product.category.dto.paginated import CategoriesShortPaginated
from app.product.category.dto.sorting import CategorySortingParams
from app.product.category.query import (
    ListShortCategories,
    ListShortCategoriesQuery,
)
from app.product.position.dto.paginated import PositionsShortPaginated
from app.product.position.dto.position import (
    PositionDTO,
    PositionWithItemsAmount,
)
from app.product.position.dto.sorting import PositionSortingParams
from app.product.position.query import (
    GetPosition,
    GetPositionQuery,
    GetPositionWithItemsAmount,
    GetPositionWithItemsAmountQuery,
    ListPositionsShortByCategory,
    ListPositionsShortByCategoryQuery,
)
from domain.common.localized import Language
from domain.product.category.enums import CategoryStatus
from domain.product.position.enums import PositionStatus
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.mapper import FileKeyMapper
from presentation.aiogram.port import Text

from .ctx import (
    CATEGORIES_PAGE_LIMIT,
    CATEGORIES_SCROLL,
    CTX_KEY,
    POSITION_MEDIA_SCROLL,
    POSITIONS_PAGE_LIMIT,
    POSITIONS_SCROLL,
    AdminPositionCtx,
)


@dataclass(slots=True, frozen=True)
class CategoryButton:
    id: UUID
    name: str

    created_at: datetime


@dataclass(slots=True, frozen=True)
class PositionButton:
    id: UUID
    name: str

    created_at: datetime


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language

    is_current: bool


@dataclass(slots=True, frozen=True)
class CategoryStatusButton:
    status: CategoryStatus

    is_current: bool


@dataclass(slots=True, frozen=True)
class PositionStatusButton:
    status: PositionStatus

    is_current: bool


@inject
async def select_category_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[ListShortCategories],
    tg_ctx: FromDishka[TelegramContextDTO],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    current_page: int = await dialog_manager.find(CATEGORIES_SCROLL).get_page()  # type: ignore[union-attr]
    offset = current_page * CATEGORIES_PAGE_LIMIT

    paginated: CategoriesShortPaginated = await query_handler(
        ListShortCategoriesQuery(
            pagination=OffsetPaginationParams(
                limit=CATEGORIES_PAGE_LIMIT,
                offset=offset,
            ),
            sorting=CategorySortingParams(
                field="created_at",
                order=ctx.category_sorting_order,
            ),
            show_with_no_items=None,
            status=ctx.category_status,
        ),
    )

    return {
        "pages": (paginated.total + CATEGORIES_PAGE_LIMIT - 1)
        // CATEGORIES_PAGE_LIMIT,
        "buttons": [
            CategoryButton(
                id=category.id,
                name=category.name.get_with_fallback(tg_ctx.lang),
                created_at=category.created_at,
            )
            for category in paginated.categories
        ],
    }


@inject
async def category_filters_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )

    return {
        "sorting_order": ctx.category_sorting_order,
        "buttons": [
            CategoryStatusButton(
                status=status,
                is_current=status == ctx.category_status,
            )
            for status in CategoryStatus
        ],
    }


@inject
async def select_position_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[ListPositionsShortByCategory],
    tg_ctx: FromDishka[TelegramContextDTO],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_category_id is None:
        return {}

    current_page: int = await dialog_manager.find(POSITIONS_SCROLL).get_page()  # type: ignore[union-attr]
    offset = current_page * POSITIONS_PAGE_LIMIT

    paginated: PositionsShortPaginated = await query_handler(
        ListPositionsShortByCategoryQuery(
            pagination=OffsetPaginationParams(
                limit=CATEGORIES_PAGE_LIMIT,
                offset=offset,
            ),
            sorting=PositionSortingParams(
                field="created_at",
                order=ctx.position_sorting_order,
            ),
            category_id=ctx.current_category_id,
            show_with_no_items=None,
            status=ctx.position_status,
        ),
    )

    return {
        "buttons": [
            PositionButton(
                id=position.id,
                name=position.name.get_with_fallback(lang=tg_ctx.lang),
                created_at=position.created_at,
            )
            for position in paginated.positions
        ],
        "pages": (paginated.total + POSITIONS_PAGE_LIMIT - 1)
        // POSITIONS_PAGE_LIMIT,
    }


@inject
async def position_filters_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )

    return {
        "sorting_order": ctx.position_sorting_order,
        "buttons": [
            PositionStatusButton(
                status=status,
                is_current=status == ctx.position_status,
            )
            for status in PositionStatus
        ],
    }


@inject
async def position_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetPositionWithItemsAmount],
    text: FromDishka[Text],
    mapper: FromDishka[FileKeyMapper],
    tg_ctx: FromDishka[TelegramContextDTO],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_position_id is None:
        return {}

    dto: PositionWithItemsAmount = await query_handler(
        GetPositionWithItemsAmountQuery(id=ctx.current_position_id),
    )
    current_page: int = await dialog_manager.find(  # type: ignore[union-attr]
        POSITION_MEDIA_SCROLL,
    ).get_page()
    media: MediaAttachment | None = None

    if dto.position.media:
        media = await mapper.to_media_attachment(
            key=AppFileKeyMapper.to_value_object(
                src=dto.position.media[current_page],
            ),
        )

    prices: list[str] = [
        text(
            "position-price-row",
            amount=price.amount,
            currency=price.currency,
            is_last=i == len(dto.position.price.prices),
        )
        for i, price in enumerate(dto.position.price.prices.values(), start=1)
    ]

    return {
        "name": dto.position.name.get(lang=ctx.current_lang),
        "description": dto.position.description.get(lang=ctx.current_lang)
        if dto.position.description
        else None,
        "has_description": bool(dto.position.description),
        "prices": "\n".join(prices),
        "updated_at": dto.position.updated_at,
        "created_at": dto.position.created_at,
        "items_amount": dto.items_amount,
        "buttons": [
            LanguageButton(lang=lang, is_current=lang == ctx.current_lang)
            for lang in Language
        ],
        "pages": len(dto.position.media),
        "media": media,
        "currency": tg_ctx.currency,
        "is_archived": dto.position.status == PositionStatus.ARCHIVED,
    }


@inject
async def archive_confirmation_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetPosition],
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_position_id is None:
        return {}

    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.current_position_id),
    )

    return {"name": position.name.get_with_fallback(lang=tg_ctx.lang)}


@inject
async def delete_confirmation_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetPosition],
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminPositionCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminPositionCtx,
    )
    if ctx.current_position_id is None:
        return {}

    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.current_position_id),
    )

    return {"name": position.name.get_with_fallback(lang=tg_ctx.lang)}
