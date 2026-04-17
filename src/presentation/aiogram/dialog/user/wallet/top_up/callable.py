from decimal import Decimal
from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.money import MoneyDTO
from app.payment.cmd import (
    CancelPayment,
    CancelPaymentCmd,
    CheckPayment,
    CheckPaymentCmd,
)
from app.payment.port.payment.dto import Invoice, InvoiceStatus
from app.wallet.cmd import (
    CreateTopUpPayment,
    CreateTopUpPaymentCmd,
)
from domain.common.money import Currency
from domain.payment.enums import PaymentMethod
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.user.wallet.top_up.ctx import (
    CTX_KEY,
    TopUpCtx,
)
from presentation.aiogram.port import Text
from presentation.aiogram.state import TopUpState


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    tg_ctx: FromDishka[TelegramContextDTO],
    retort: FromDishka[Retort],
) -> None:
    ctx = TopUpCtx(current_currency=tg_ctx.currency)

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_amount(
    event: Message,
    widget: ManagedTextInput[Decimal],
    dialog_manager: DialogManager,
    amount: Decimal,
    retort: FromDishka[Retort],
) -> None:
    await event.delete()

    ctx: TopUpCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], TopUpCtx)
    ctx.top_up_amount = amount
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await dialog_manager.switch_to(
        state=TopUpState.select_payment_method,
        show_mode=ShowMode.EDIT,
    )


@inject
async def on_select_currency(
    event: CallbackQuery,
    widget: ManagedTextInput[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    retort: FromDishka[Retort],
) -> None:
    ctx: TopUpCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], TopUpCtx)
    ctx.current_currency = currency
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_payment_method(
    event: CallbackQuery,
    widget: Select[PaymentMethod],
    dialog_manager: DialogManager,
    method: PaymentMethod,
    handler: FromDishka[CreateTopUpPayment],
    retort: FromDishka[Retort],
) -> None:
    ctx: TopUpCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], TopUpCtx)
    if ctx.top_up_amount is None:
        return None

    invoice: Invoice = await handler(
        CreateTopUpPaymentCmd(
            amount=MoneyDTO(
                amount=ctx.top_up_amount,
                currency=ctx.current_currency,
            ),
            method=method,
        ),
    )
    ctx.invoice = invoice
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    return await dialog_manager.switch_to(state=TopUpState.payment)


@inject
async def on_check(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[CheckPayment],
    text: FromDishka[Text],
    retort: FromDishka[Retort],
) -> None:
    ctx: TopUpCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], TopUpCtx)
    if ctx.invoice is None:
        return

    invoice: Invoice = await handler(
        CheckPaymentCmd(id=ctx.invoice.payment_id),
    )

    await event.answer(
        text=text("top-up-payment.check", status=invoice.status),
    )

    if invoice.status == InvoiceStatus.PAID:
        await dialog_manager.done()


@inject
async def on_cancel(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[CancelPayment],
    text: FromDishka[Text],
    retort: FromDishka[Retort],
) -> None:
    ctx: TopUpCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], TopUpCtx)
    if ctx.invoice is None:
        return

    await handler(
        CancelPaymentCmd(
            id=ctx.invoice.payment_id,
        ),
    )
    await event.answer(text=text("top-up-payment.cancel"))
    await dialog_manager.done()
