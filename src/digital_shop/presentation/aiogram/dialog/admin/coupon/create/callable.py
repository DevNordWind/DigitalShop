from datetime import datetime
from decimal import Decimal
from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from app.common.dto.coefficient import CoefficientMapper
from app.common.dto.money import MoneyDTO, MoneyMapper
from app.coupon.cmd import CreateCoupon, CreateCouponCmd
from app.coupon.dto.discount import (
    CoefficientDiscountDTO,
    FixedAmountDiscountDTO,
)
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.coefficient import Coefficient
from domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRateGateway,
)
from domain.common.money import Currency, Money
from domain.common.port import Clock
from domain.coupon.enums import CouponType
from domain.coupon.value_object import CouponCode, CouponValidity
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.port import Text
from presentation.aiogram.state import CreateCouponState

from .ctx import CTX_KEY, CouponCreationCtx


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
) -> None:
    ctx = CouponCreationCtx(current_currency=tg_ctx.currency)
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_code(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    code: str,
    retort: FromDishka[Retort],
) -> None:
    CouponCode(value=code)
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    ctx.code = code

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await event.delete()
    await dialog_manager.switch_to(
        state=CreateCouponState.view, show_mode=ShowMode.EDIT
    )


async def on_select_type(
    event: CallbackQuery,
    widget: Select[CouponType],
    dialog_manager: DialogManager,
    tp: CouponType,
) -> None:
    if tp == CouponType.FIXED:
        return await dialog_manager.switch_to(
            state=CreateCouponState.input_amount,
        )

    return await dialog_manager.switch_to(
        state=CreateCouponState.input_percent,
    )


@inject
async def on_input_amount(
    event: Message,
    widget: ManagedTextInput[Decimal],
    dialog_manager: DialogManager,
    amount: Decimal,
    retort: FromDishka[Retort],
) -> None:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    current_discounts: dict[Currency, MoneyDTO] = {}
    if isinstance(ctx.discount, FixedAmountDiscountDTO):
        current_discounts = ctx.discount.discounts

    money: MoneyDTO = MoneyDTO(amount=amount, currency=ctx.current_currency)

    ctx.discount = FixedAmountDiscountDTO(
        type=CouponType.FIXED,
        discounts=current_discounts | {ctx.current_currency: money},
    )

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    dialog_manager.show_mode = ShowMode.EDIT
    await event.delete()


@inject
async def on_select_currency(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    retort: FromDishka[Retort],
) -> None:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    ctx.current_currency = currency
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_percent(
    event: Message,
    widget: ManagedTextInput[Decimal],
    dialog_manager: DialogManager,
    amount: Decimal,
    retort: FromDishka[Retort],
) -> None:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )

    coefficient = Coefficient(value=amount / Decimal("100.0"))

    ctx.discount = CoefficientDiscountDTO(
        type=CouponType.COEFFICIENT,
        coefficient=CoefficientMapper.to_dto(coefficient),
    )

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await event.delete()
    await dialog_manager.switch_to(
        state=CreateCouponState.select_type,
        show_mode=ShowMode.EDIT,
    )


@inject
async def on_convert_to_other(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    rate_gateway: FromDishka[ExchangeRateGateway],
) -> None:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    if (
        ctx.current_currency is None
        or not isinstance(ctx.discount, FixedAmountDiscountDTO)
        or ctx.current_currency not in ctx.discount.discounts
    ):
        return

    source = Money(
        currency=ctx.current_currency,
        amount=ctx.discount.discounts[ctx.current_currency].amount,
    )
    pairs = [
        CurrencyPair(source=source.currency, target=currency)
        for currency in Currency
        if currency != source.currency
    ]
    rates = await rate_gateway.get_many(pairs)
    source_dto = MoneyMapper.to_dto(source)

    ctx.discount = FixedAmountDiscountDTO(
        type=CouponType.FIXED,
        discounts={
            rate.pair.target: MoneyMapper.to_dto(src=rate.convert(source))
            for rate in rates
        }
        | {source_dto.currency: source_dto},
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_clear_amount(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    if not isinstance(ctx.discount, FixedAmountDiscountDTO):
        return

    ctx.discount = FixedAmountDiscountDTO(
        type=CouponType.FIXED,
        discounts={
            currency: discount
            for currency, discount in ctx.discount.discounts.items()
            if currency != ctx.current_currency
        },
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_confirm(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[CreateCoupon],
) -> None:
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    if ctx.code is None or ctx.discount is None:
        return

    await handler(
        CreateCouponCmd(
            code=ctx.code,
            discount=ctx.discount,
            valid_from=ctx.valid_from,
            valid_until=ctx.valid_until,
        ),
    )
    await dialog_manager.done()


@inject
async def on_input_valid_from(
    event: Message,
    widget: ManagedTextInput[datetime],
    dialog_manager: DialogManager,
    valid_from: datetime,
    retort: FromDishka[Retort],
    clock: FromDishka[Clock],
) -> None:
    now: datetime = clock.now()
    CouponValidity.create(now=now, value=valid_from)

    await event.delete()
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )
    ctx.valid_from = valid_from

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await dialog_manager.switch_to(
        state=CreateCouponState.view,
        show_mode=ShowMode.EDIT,
    )


@inject
async def on_input_valid_until(
    event: Message,
    widget: ManagedTextInput[datetime],
    dialog_manager: DialogManager,
    valid_from: datetime,
    retort: FromDishka[Retort],
    clock: FromDishka[Clock],
) -> None:
    now: datetime = clock.now()
    CouponValidity.create(now=now, value=valid_from)

    await event.delete()
    ctx: CouponCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CouponCreationCtx,
    )

    ctx.valid_until = valid_from

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await dialog_manager.switch_to(
        state=CreateCouponState.view,
        show_mode=ShowMode.EDIT,
    )


@inject
async def on_date_error(
    message: Message,
    widget: ManagedTextInput[datetime],
    dialog_manager: DialogManager,
    error: ValueError,
    t: FromDishka[Text],
) -> Message:
    return await message.reply(text=t("admin-coupon-create-invalid-date"))
