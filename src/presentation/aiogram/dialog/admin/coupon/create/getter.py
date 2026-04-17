from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.money import MoneyDTO
from app.coupon.dto.discount import (
    CoefficientDiscountDTO,
    FixedAmountDiscountDTO,
)
from domain.common.money import Currency
from domain.coupon.enums import CouponType
from presentation.aiogram.dialog.admin.coupon.create.ctx import (
    CTX_KEY,
    CouponCreationCtx,
)
from presentation.aiogram.port import Text


@dataclass(slots=True, frozen=True)
class CouponTypeButton:
    type: CouponType


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


SELECT_TYPE_BUTTONS: tuple[CouponTypeButton, ...] = tuple(
    CouponTypeButton(type=tp) for tp in CouponType
)


@inject
async def view_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    text: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    percent: Decimal | None = None
    amounts: list[str] = []

    if isinstance(ctx.discount, CoefficientDiscountDTO):
        percent = ctx.discount.as_percent

    elif isinstance(ctx.discount, FixedAmountDiscountDTO):
        amounts = [
            text(
                "coupon-amount-row",
                amount=money.amount,
                currency=money.currency,
                is_last=i == len(ctx.discount.discounts),
            )
            for i, money in enumerate(ctx.discount.discounts.values())
        ]

    return {
        "valid_from": ctx.valid_from,
        "valid_until": ctx.valid_until,
        "code": ctx.code,
        "type": ctx.discount.type if ctx.discount else None,
        "can_create": ctx.can_create,
        "amounts": "\n".join(amounts),
        "percent": percent,
    }


@inject
async def select_type_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    text: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    percent: Decimal | None = None
    amounts: list[str] = []

    if isinstance(ctx.discount, CoefficientDiscountDTO):
        percent = ctx.discount.as_percent

    elif isinstance(ctx.discount, FixedAmountDiscountDTO):
        amounts = [
            text(
                "coupon-amount-row",
                amount=money.amount,
                currency=money.currency,
            )
            for money in ctx.discount.discounts.values()
        ]

    return {
        "type": ctx.discount.type if ctx.discount else None,
        "amounts": "\n".join(amounts),
        "percent": percent,
        "buttons": SELECT_TYPE_BUTTONS,
    }


@inject
async def input_code_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    return {"code": ctx.code}


@inject
async def input_amount_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    text: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    amounts: list[str] = []
    can_convert_to_other: bool = False
    can_clear: bool = False
    if isinstance(ctx.discount, FixedAmountDiscountDTO):
        amounts = [
            text(
                "coupon-amount-row",
                amount=money.amount,
                currency=money.currency,
                is_last=i == len(ctx.discount.discounts),
            )
            for i, money in enumerate(ctx.discount.discounts.values(), start=1)
        ]
        current_discount: MoneyDTO | None = ctx.discount.discounts.get(
            ctx.current_currency,
        )
        can_clear = current_discount is not None
        can_convert_to_other = current_discount is not None and len(
            ctx.discount.discounts,
        ) != len(Currency)

    return {
        "buttons": [
            CurrencyButton(
                currency=currency,
                is_current=currency == ctx.current_currency,
            )
            for currency in Currency
        ],
        "can_convert_to_other": can_convert_to_other,
        "amounts": "\n".join(amounts) or None,
        "can_clear": can_clear,
    }
