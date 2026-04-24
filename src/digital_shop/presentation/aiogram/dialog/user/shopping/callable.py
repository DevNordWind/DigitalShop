from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from app.order.cmd import CreateOrder, CreateOrderCmd
from dishka import AsyncContainer, FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.order.value_object import OrderId
from domain.product.position.enums import WarehouseType
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.user.shopping.ctx import CTX_KEY, ShoppingCtx
from presentation.aiogram.state import OrderState, ShoppingState


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = ShoppingCtx(
        current_category_id=None,
        current_position_id=None,
        current_position_warehouse_type=None,
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_category(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    category_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: ShoppingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ShoppingCtx,
    )
    ctx.current_category_id = category_id
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(ShoppingState.select_position)


@inject
async def on_select_position(
    event: CallbackQuery,
    select: Select[UUID],
    dialog_manager: DialogManager,
    position_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: ShoppingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ShoppingCtx,
    )
    ctx.current_position_id = position_id

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(ShoppingState.position)


@inject
async def on_buy(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[CreateOrder],
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
    container: FromDishka[AsyncContainer],
) -> None:
    ctx: ShoppingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ShoppingCtx,
    )
    if (
        ctx.current_position_warehouse_type is None
        or ctx.current_position_id is None
    ):
        return None

    if ctx.current_position_warehouse_type == WarehouseType.FIXED:
        order_id: OrderId = await handler(
            CreateOrderCmd(
                position_id=ctx.current_position_id,
                items_amount=1,
                customer_currency=tg_ctx.currency,
            ),
        )
        await container.close()
        return await dialog_manager.start(
            state=OrderState.order,
            data={"order_id": order_id.value},
        )

    return await dialog_manager.switch_to(
        state=ShoppingState.input_items_amount,
    )


@inject
async def on_input_items_amount(
    event: Message,
    widget: ManagedTextInput[int],
    dialog_manager: DialogManager,
    items_amount: int,
    handler: FromDishka[CreateOrder],
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
) -> None:
    ctx: ShoppingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ShoppingCtx,
    )
    if ctx.current_position_id is None:
        return None

    order_id: OrderId = await handler(
        CreateOrderCmd(
            position_id=ctx.current_position_id,
            items_amount=items_amount,
            customer_currency=tg_ctx.currency,
        ),
    )
    await event.delete()

    return await dialog_manager.start(
        state=OrderState.order,
        data={"order_id": order_id.value},
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )
