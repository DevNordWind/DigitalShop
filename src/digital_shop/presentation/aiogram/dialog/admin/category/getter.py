from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from app.common.dto.file_key import FileKeyDTO
from app.common.dto.file_key import FileKeyMapper as AppFileKeyMapper
from app.common.dto.query_params import (
    OffsetPaginationParams,
)
from app.product.category.dto.category import (
    CategoryShortDTO,
    CategoryWithGoodsAmountDTO,
)
from app.product.category.dto.paginated import CategoriesShortPaginated
from app.product.category.dto.sorting import CategorySortingParams
from app.product.category.query import (
    GetCategoryShort,
    GetCategoryShortQuery,
    ListShortCategories,
    ListShortCategoriesQuery,
)
from app.product.category.query.get_with_goods_amount import (
    GetCategoryWithGoodsAmount,
    GetCategoryWithGoodsAmountQuery,
)
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from domain.product.category.enums import CategoryStatus
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.admin.category.const import (
    CATEGORIES_PAGE_LIMIT,
    CATEGORIES_SCROLL,
)
from presentation.aiogram.dialog.admin.category.ctx import (
    CTX_KEY,
    AdminCategoryCtx,
)
from presentation.aiogram.mapper import FileKeyMapper


@dataclass(slots=True, frozen=True)
class CategoryButton:
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


@inject
async def categories_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[ListShortCategories],
    tg_ctx: FromDishka[TelegramContextDTO],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    current_page: int = await dialog_manager.find(CATEGORIES_SCROLL).get_page()  # type: ignore[union-attr]
    offset = current_page * CATEGORIES_PAGE_LIMIT
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )

    paginated: CategoriesShortPaginated = await query_handler(
        ListShortCategoriesQuery(
            pagination=OffsetPaginationParams(
                limit=CATEGORIES_PAGE_LIMIT,
                offset=offset,
            ),
            sorting=CategorySortingParams(
                field="created_at",
                order=ctx.sorting_order,
            ),
            show_with_no_items=None,
            status=ctx.status,
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
async def category_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetCategoryWithGoodsAmount],
    mapper: FromDishka[FileKeyMapper],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.current_category_id is None:
        return {}

    dto: CategoryWithGoodsAmountDTO = await query_handler(
        GetCategoryWithGoodsAmountQuery(id=ctx.current_category_id),
    )
    category = dto.category

    attachment: MediaAttachment | None = None
    if isinstance(category.media, FileKeyDTO):
        key = AppFileKeyMapper.to_value_object(src=category.media)
        attachment = await mapper.to_media_attachment(key=key)

    return {
        "name": category.name.get(lang=ctx.current_lang),
        "description": category.description.get(ctx.current_lang)
        if category.description
        else None,
        "has_description": bool(category.description),
        "positions_amount": dto.positions_amount,
        "items_amount": dto.items_amount,
        "created_at": category.created_at,
        "updated_at": category.updated_at,
        "media": attachment,
        "buttons": [
            LanguageButton(lang=lang, is_current=ctx.current_lang == lang)
            for lang in Language
        ],
        "archived_at": category.archived_at,
        "is_archived": category.status == CategoryStatus.ARCHIVED,
    }


@inject
async def archive_confirmation_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetCategoryShort],
    tg_ctx: FromDishka[TelegramContextDTO],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.current_category_id is None:
        return {}

    dto: CategoryShortDTO = await query_handler(
        GetCategoryShortQuery(id=ctx.current_category_id),
    )

    return {"name": dto.name.get_with_fallback(tg_ctx.lang)}


@inject
async def delete_confirmation_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetCategoryShort],
    tg_ctx: FromDishka[TelegramContextDTO],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )
    if ctx.current_category_id is None:
        return {}

    dto: CategoryShortDTO = await query_handler(
        GetCategoryShortQuery(id=ctx.current_category_id),
    )

    return {"name": dto.name.get_with_fallback(tg_ctx.lang)}


@inject
async def filters_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminCategoryCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCategoryCtx,
    )

    return {
        "buttons": [
            CategoryStatusButton(
                status=status,
                is_current=status == ctx.status,
            )
            for status in CategoryStatus
        ],
        "sorting_order": ctx.sorting_order,
    }
