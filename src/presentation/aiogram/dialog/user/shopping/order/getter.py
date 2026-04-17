from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.money import MoneyDTO
from app.coupon.dto.coupon import CouponDTO
from app.coupon.dto.discount import (
    CoefficientDiscountDTO,
    FixedAmountDiscountDTO,
)
from app.order.dto.order import OrderDTO, PublicOrderDTO
from app.order.query import GetOrder, GetOrderQuery
from app.product.position.dto.position import PositionWithItemsAmount
from app.product.position.query import (
    GetPositionWithItemsAmount,
    GetPositionWithItemsAmountQuery,
)
from domain.common.money import Currency
from domain.payment.enums import PaymentMethod
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.user.shopping.order.ctx import (
    CTX_KEY,
    OrderCtx,
)
from presentation.aiogram.port import Text
from presentation.aiogram.setting.payment.model import PaymentSettings
from presentation.aiogram.setting.payment.port import PaymentSettingsGateway


@dataclass(slots=True, frozen=True)
class OrderPaymentMethodButton:
    method: PaymentMethod


@inject
async def order_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetOrder],
    tg_ctx: FromDishka[TelegramContextDTO],
    text: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)
    order: PublicOrderDTO | OrderDTO = await query_handler(
        GetOrderQuery(id=ctx.order_id),
    )

    return {
        "order_id": order.id,
        "items_amount": order.items_amount,
        "position_name": order.position.position_name.get_with_fallback(
            lang=tg_ctx.lang,
        ),
        "is_applied_coupon": bool(order.applied_coupon),
        "code": order.coupon.code if order.coupon else None,
        "total_amount": order.total.amount,
        "currency": order.total.currency,
        **_adapt_coupon_to_ftl(
            order_currency=order.total.currency,
            coupon=order.coupon,
            text=text,
        ),
        "can_confirm": order.total.amount == Decimal("0.00")
        and order.applied_coupon is not None,
    }


@inject
async def payment_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)
    if ctx.invoice is None:
        return {}

    return {
        "order_id": ctx.order_id,
        "payment_id": ctx.invoice.payment_id,
        "to_pay_amount": ctx.invoice.to_pay.amount,
        "currency": ctx.invoice.to_pay.currency,
        "method": ctx.invoice.payment_method,
        "pay_url": ctx.invoice.pay_url,
    }


@inject
async def input_new_items_amount_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    order_handler: FromDishka[GetOrder],
    position_handler: FromDishka[GetPositionWithItemsAmount],
    **_: Any,
) -> dict[str, Any]:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)
    order: OrderDTO | PublicOrderDTO = await order_handler(
        GetOrderQuery(id=ctx.order_id),
    )
    position: PositionWithItemsAmount = await position_handler(
        GetPositionWithItemsAmountQuery(id=order.position.position_id),
    )

    return {"available": position.items_amount}


@inject
async def select_payment_method_getter(
    settings_gw: FromDishka[PaymentSettingsGateway],
    **_: Any,
) -> dict[str, Any]:
    settings: list[PaymentSettings] = await settings_gw.get()

    return {
        "buttons": [
            OrderPaymentMethodButton(method=setting.method)
            for setting in settings
            if setting.is_active
        ],
    }


def _adapt_coupon_to_ftl(
    order_currency: Currency,
    coupon: CouponDTO | None,
    text: Text,
) -> dict[str, Any]:
    if coupon is None:
        return {"is_applied_coupon": False}

    amount: MoneyDTO | None = None
    percent: Decimal | None = None
    match coupon.discount:
        case FixedAmountDiscountDTO():
            amount = coupon.discount.get(currency=order_currency)
        case CoefficientDiscountDTO():
            percent = coupon.discount.as_percent

    return {
        "is_applied_coupon": True,
        "code": coupon.code,
        "coupon_discount": text(
            "coupon-discount",
            percent=percent,
            amount=amount.amount if amount is not None else None,
            currency=amount.currency if amount is not None else None,
            type=coupon.discount.type,
        ),
    }
