from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import AsyncContainer, FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.order.cmd import (
    ApplyCouponToOrder,
    ApplyCouponToOrderCmd,
    CancelOrder,
    CancelOrderCmd,
    ChangeOrderItemsAmount,
    ChangeOrderItemsAmountCmd,
    ConfirmOrderWithDiscount,
    ConfirmOrderWithDiscountCmd,
    PayOrderWithPayment,
    PayOrderWithPaymentCmd,
    PayOrderWithWallet,
    PayOrderWithWalletCmd,
)
from app.payment.cmd import CheckPayment, CheckPaymentCmd
from app.payment.port.payment import Invoice
from app.payment.port.payment.dto import InvoiceStatus
from domain.order.exception import (
    OrderCancellationForbidden,
    OrderConfirmationForbidden,
)
from domain.payment.enums import PaymentMethod
from domain.payment.exception import PaymentConfirmationForbidden
from domain.product.position.exception import OutOfStock
from presentation.aiogram.dialog.user.shopping.order.ctx import (
    CTX_KEY,
    OrderCtx,
)
from presentation.aiogram.port import Text
from presentation.aiogram.state import OrdersState, OrderState


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    if isinstance(data, dict):
        ctx = OrderCtx(order_id=data["order_id"])
        dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_cancel(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[CancelOrder],
    retort: FromDishka[Retort],
    text: FromDishka[Text],
) -> None:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)
    try:
        await handler(CancelOrderCmd(id=ctx.order_id))
    except OrderCancellationForbidden as e:
        await event.answer(
            text=text(f"{e.__class__.__name__}.call"), show_alert=True
        )
        await dialog_manager.done()
        await event.message.delete()  # type: ignore[union-attr]
        return

    await event.answer(
        text=text("user-shopping-order.order-cancelled-call"),
        show_alert=True,
    )
    await dialog_manager.done()
    await event.message.delete()  # type: ignore[union-attr]


@inject
async def on_input_coupon_code(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    code: str,
    handler: FromDishka[ApplyCouponToOrder],
    retort: FromDishka[Retort],
) -> None:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)

    await handler(
        ApplyCouponToOrderCmd(order_id=ctx.order_id, coupon_code=code),
    )

    await event.delete()
    await dialog_manager.switch_to(
        state=OrderState.order,
        show_mode=ShowMode.EDIT,
    )


@inject
async def on_pay_with_wallet(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[PayOrderWithWallet],
    retort: FromDishka[Retort],
    text: FromDishka[Text],
) -> None:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)

    try:
        await handler(cmd=PayOrderWithWalletCmd(order_id=ctx.order_id))
    except OutOfStock as e:
        if e.available == 0:
            await event.answer(
                text=text(
                    "user-shopping-order-payment.no-items-available-call",
                ),
            )
            await event.message.delete()  # type: ignore[union-attr]
            return await dialog_manager.done()

        return await dialog_manager.switch_to(
            state=OrderState.input_new_items_amount,
        )
    return await dialog_manager.start(
        state=OrdersState.order,
        data={"order_id": ctx.order_id},
        mode=StartMode.RESET_STACK,
    )


@inject
async def on_select_payment_method(
    event: CallbackQuery,
    widget: Select[PaymentMethod],
    dialog_manager: DialogManager,
    method: PaymentMethod,
    handler: FromDishka[PayOrderWithPayment],
    text: FromDishka[Text],
    retort: FromDishka[Retort],
) -> None:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)
    try:
        invoice: Invoice = await handler(
            PayOrderWithPaymentCmd(order_id=ctx.order_id, method=method),
        )
    except OutOfStock as e:
        if e.available == 0:
            await event.answer(
                text=text(
                    "user-shopping-order-payment.no-items-available-call",
                ),
            )
            await event.message.delete()  # type: ignore[union-attr]
            return await dialog_manager.done()

        return await dialog_manager.switch_to(
            state=OrderState.input_new_items_amount,
        )

    ctx.invoice = invoice
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    return await dialog_manager.switch_to(
        state=OrderState.payment,
    )


@inject
async def on_input_new_items_amount(
    event: Message,
    widget: ManagedTextInput[int],
    dialog_manager: DialogManager,
    items_amount: int,
    handler: FromDishka[ChangeOrderItemsAmount],
    retort: FromDishka[Retort],
    t: FromDishka[Text],
) -> Message | None:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)

    try:
        await handler(
            ChangeOrderItemsAmountCmd(
                id=ctx.order_id,
                new_items_amount=items_amount,
            ),
        )
    except OutOfStock as e:
        if e.available == 0:
            await event.reply(
                text=t("user-shopping-order-new-items.cancel-msg"),
            )
            await dialog_manager.done()
            return None

        return await event.reply(
            text=t(key=e.__class__.__name__, available=e.available)
        )

    await event.delete()
    await dialog_manager.switch_to(
        state=OrderState.order,
        show_mode=ShowMode.EDIT,
    )
    return None


@inject
async def on_check(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[CheckPayment],
    text: FromDishka[Text],
    container: FromDishka[AsyncContainer],
) -> None:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)
    if ctx.invoice is None:
        return None
    try:
        invoice: Invoice = await handler(
            CheckPaymentCmd(id=ctx.invoice.payment_id),
        )
    except (OrderConfirmationForbidden, PaymentConfirmationForbidden) as e:
        await event.answer(
            text=text(f"{e.__class__.__name__}.call"), show_alert=True
        )
        await event.message.delete()  # type: ignore[union-attr]
        return await dialog_manager.start(
            state=OrdersState.order,
            data={"order_id": ctx.order_id},
            mode=StartMode.RESET_STACK,
        )

    await event.answer(
        text=text("user-shopping-order-payment.check", status=invoice.status),
    )
    if invoice.status == InvoiceStatus.PAID:
        await event.message.delete()  # type: ignore[union-attr]
        await container.close()
        return await dialog_manager.start(
            state=OrdersState.order,
            data={"order_id": ctx.order_id},
            mode=StartMode.RESET_STACK,
        )

    return None


@inject
async def on_confirm_order_with_discount(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[ConfirmOrderWithDiscount],
    retort: FromDishka[Retort],
) -> None:
    ctx: OrderCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], OrderCtx)
    await handler(ConfirmOrderWithDiscountCmd(order_id=ctx.order_id))
    await dialog_manager.start(
        state=OrdersState.order,
        data={"order_id": ctx.order_id},
        mode=StartMode.RESET_STACK,
    )
