from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.query_params import OffsetPaginationParams
from app.coupon.dto.coupon import CouponDTO
from app.coupon.dto.discount import (
    CoefficientDiscountDTO,
    FixedAmountDiscountDTO,
)
from app.coupon.dto.paginated import CouponsPaginated
from app.coupon.query import (
    GetCoupon,
    GetCouponQuery,
    ListCoupons,
    ListCouponsQuery,
)
from domain.coupon.enums import CouponStatus, CouponType
from presentation.aiogram.dialog.admin.coupon.ctx import (
    COUPONS_HEIGHT,
    COUPONS_SCROLL,
    CTX_KEY,
    AdminCouponCtx,
)
from presentation.aiogram.port import Text


@dataclass(slots=True, frozen=True)
class CouponButton:
    id: UUID

    code: str
    type: CouponType

    percent: Decimal | None


@dataclass(slots=True, frozen=True)
class CouponStatusButton:
    status: CouponStatus

    is_current: bool


@inject
async def coupons_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[ListCoupons],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminCouponCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCouponCtx,
    )
    current_page: int = await dialog_manager.find(COUPONS_SCROLL).get_page()  # type: ignore[union-attr]
    offset: int = current_page * COUPONS_HEIGHT

    paginated: CouponsPaginated = await query_handler(
        query=ListCouponsQuery(
            sorting=ctx.sorting,
            pagination=OffsetPaginationParams(
                limit=COUPONS_HEIGHT,
                offset=offset,
            ),
            status=ctx.status,
        ),
    )

    return {
        "pages": (paginated.total + COUPONS_HEIGHT - 1) // COUPONS_HEIGHT,
        "buttons": [
            CouponButton(
                id=coupon.id,
                code=coupon.code,
                type=coupon.discount.type,
                percent=coupon.discount.as_percent
                if isinstance(coupon.discount, CoefficientDiscountDTO)
                else None,
            )
            for coupon in paginated.coupons
        ],
    }


@inject
async def coupon_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetCoupon],
    text: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminCouponCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCouponCtx,
    )
    if ctx.current_coupon_id is None:
        return {}

    coupon: CouponDTO = await query_handler(
        GetCouponQuery(id=ctx.current_coupon_id),
    )
    percent: Decimal | None = None
    amounts: list[str] = []

    if isinstance(coupon.discount, CoefficientDiscountDTO):
        percent = coupon.discount.as_percent

    elif isinstance(coupon.discount, FixedAmountDiscountDTO):
        amounts = [
            text(
                "coupon-amount-row",
                amount=money.amount,
                currency=money.currency,
                is_last=i == len(coupon.discount.discounts),
            )
            for i, money in enumerate(
                coupon.discount.discounts.values(),
                start=1,
            )
        ]

    return {
        "code": coupon.code,
        "type": coupon.discount.type,
        "percent": percent,
        "amounts": "\n".join(amounts),
        "is_revoked": coupon.is_revoked,
        "valid_from": coupon.valid_from,
        "valid_until": coupon.valid_until,
    }


@inject
async def filters_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminCouponCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCouponCtx,
    )

    return {
        "sorting_order": ctx.sorting.order,
        "buttons": [
            CouponStatusButton(status=status, is_current=status == ctx.status)
            for status in CouponStatus
        ],
    }
