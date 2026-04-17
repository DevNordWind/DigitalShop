from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.query_params import OffsetPaginationParams
from app.order.dto.order import OrderDTO, PublicOrderDTO
from app.order.dto.paginated import OrdersPaginated
from app.order.dto.sorting import OrderSortingParams
from app.order.query import (
    GetOrder,
    GetOrderQuery,
    ListOrders,
    ListOrdersQuery,
)
from domain.order.enums import OrderStatus
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.user.profile.order.ctx import (
    CTX_KEY,
    ORDER_HEIGHT,
    ORDER_SCROLL,
    OrdersCtx,
)
from presentation.aiogram.port import Text


@dataclass(slots=True, frozen=True)
class OrderButton:
    id: UUID

    position_name: str
    count: int

    created_at: datetime


@dataclass(slots=True, frozen=True)
class OrderStatusButton:
    status: OrderStatus

    is_current: bool


@inject
async def orders_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[ListOrders],
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    ctx: OrdersCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        OrdersCtx,
    )
    current_page: int = await dialog_manager.find(ORDER_SCROLL).get_page()  # type: ignore[union-attr]
    offset: int = current_page * ORDER_HEIGHT

    paginated: OrdersPaginated = await query_handler(
        ListOrdersQuery(
            customer_id=ctx.current_user_id,
            sorting=OrderSortingParams(
                field="created_at",
                order=ctx.filters.sorting_order,
            ),
            pagination=OffsetPaginationParams(
                limit=ORDER_HEIGHT,
                offset=offset,
            ),
            status=ctx.filters.status,
        ),
    )

    return {
        "pages": (paginated.total + ORDER_HEIGHT - 1) // ORDER_HEIGHT,
        "buttons": [
            OrderButton(
                id=order.id,
                position_name=order.position.position_name.get_with_fallback(
                    lang=tg_ctx.lang,
                ),
                count=order.items_amount,
                created_at=order.created_at,
            )
            for order in paginated.orders
        ],
    }


@inject
async def filters_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: OrdersCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        OrdersCtx,
    )

    return {
        "sorting_order": ctx.filters.sorting_order,
        "buttons": [
            OrderStatusButton(
                status=status,
                is_current=status == ctx.filters.status,
            )
            for status in OrderStatus
            if status != OrderStatus.FAILED
        ],
    }


@inject
async def order_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetOrder],
    tg_ctx: FromDishka[TelegramContextDTO],
    t: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: OrdersCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        OrdersCtx,
    )
    if ctx.current_order_id is None:
        return {}

    order: OrderDTO | PublicOrderDTO = await query_handler(
        GetOrderQuery(id=ctx.current_order_id),
    )
    coupon_row: str | None = None
    is_applied_coupon: bool = False
    if order.coupon is not None and order.applied_coupon is not None:
        is_applied_coupon = True
        coupon_row = t(
            "user-order-coupon",
            code=order.coupon.code,
            amount=order.applied_coupon.discount.amount,
            currency=order.applied_coupon.discount.currency,
        )

    return {
        "position_name": order.position.position_name.get_with_fallback(
            lang=tg_ctx.lang,
        ),
        "order_id": order.id,
        "total_amount": order.total.amount,
        "currency": order.total.currency,
        "items_amount": order.items_amount,
        "is_applied_coupon": is_applied_coupon,
        "coupon_row": coupon_row,
        "status": order.status,
        "confirmed_at": order.confirmed_at,
        "cancelled_at": order.cancelled_at,
        "failed_at": order.failed_at,
        "can_view_items": isinstance(order, OrderDTO) and order.items,
        "method": getattr(order.source, "payment_method", None),
        "source_type": getattr(order.source, "type", None),
        "has_source": order.source is not None,
    }
