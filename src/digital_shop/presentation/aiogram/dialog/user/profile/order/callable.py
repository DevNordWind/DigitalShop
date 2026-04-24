from uuid import UUID

from adaptix import Retort
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import Data, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Select
from app.common.dto.query_params import SortingOrder
from app.order.dto.order import OrderDTO, PublicOrderDTO
from app.order.query import GetOrder, GetOrderQuery
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.order.enums import OrderStatus
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.user.profile.order.ctx import (
    CTX_KEY,
    OrdersCtx,
    OrdersFilters,
)
from presentation.aiogram.kb import ServiceKeyboard
from presentation.aiogram.state import OrdersState


@inject
async def on_start(
    data: Data,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
) -> None:
    current_order_id: UUID | None = None
    current_user_id: UUID | None = None

    if isinstance(data, dict):
        current_order_id = data.get("order_id")
        current_user_id = data.get("current_user_id")

    ctx = OrdersCtx(
        filters=OrdersFilters(sorting_order=SortingOrder.DESC, status=None),
        current_order_id=current_order_id,
        current_user_id=current_user_id
        if current_user_id is not None
        else tg_ctx.user_id,
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_sorting_order(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: OrdersCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        OrdersCtx,
    )
    ctx.filters.sorting_order = (
        SortingOrder.DESC
        if ctx.filters.sorting_order == SortingOrder.ASC
        else SortingOrder.ASC
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_order_status(
    event: CallbackQuery,
    widget: Select[OrderStatus],
    dialog_manager: DialogManager,
    status: OrderStatus,
    retort: FromDishka[Retort],
) -> None:
    ctx: OrdersCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        OrdersCtx,
    )
    if ctx.filters.status == status:
        ctx.filters.status = None
    else:
        ctx.filters.status = status

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_order(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    order_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: OrdersCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        OrdersCtx,
    )
    ctx.current_order_id = order_id
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await dialog_manager.switch_to(state=OrdersState.order)


@inject
async def on_upload_items(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    kb: FromDishka[ServiceKeyboard],
    handler: FromDishka[GetOrder],
) -> None:
    ctx: OrdersCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        OrdersCtx,
    )
    if ctx.current_order_id is None:
        return

    order: OrderDTO | PublicOrderDTO = await handler(
        GetOrderQuery(id=ctx.current_order_id)
    )
    if not isinstance(order, OrderDTO) or order.items is None:
        return

    bot: Bot = dialog_manager.middleware_data["bot"]
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    items: str = "\n".join([item.item_content.value for item in order.items])

    await bot.send_message(
        text=items,
        chat_id=event.message.chat.id,  # type: ignore[union-attr]
        reply_markup=kb.get_order_items_markups(items=items),
    )
