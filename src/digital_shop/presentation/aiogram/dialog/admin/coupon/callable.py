from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from app.common.dto.query_params import SortingOrder
from app.coupon.cmd import (
    RevokeCoupon,
    RevokeCouponCmd,
)
from app.coupon.dto.sorting import CouponSortingParams
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.coupon.enums import CouponStatus
from presentation.aiogram.dialog.admin.coupon.ctx import (
    CTX_KEY,
    AdminCouponCtx,
)
from presentation.aiogram.state import AdminCouponState


@inject
async def on_start(
    _: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = AdminCouponCtx()
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_sorting_order(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCouponCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCouponCtx,
    )
    new_order: SortingOrder = (
        SortingOrder.DESC
        if ctx.sorting.order == SortingOrder.ASC
        else SortingOrder.ASC
    )
    ctx.sorting = CouponSortingParams(field="created_at", order=new_order)
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_coupon_status(
    event: CallbackQuery,
    widget: Select[CouponStatus],
    dialog_manager: DialogManager,
    coupon_status: CouponStatus,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCouponCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCouponCtx,
    )
    if ctx.status == coupon_status:
        ctx.status = None
    else:
        ctx.status = coupon_status

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_coupon(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    coupon_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminCouponCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCouponCtx,
    )
    ctx.current_coupon_id = coupon_id

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(state=AdminCouponState.coupon)


@inject
async def on_revoke(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[RevokeCoupon],
) -> None:
    ctx: AdminCouponCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        AdminCouponCtx,
    )
    if ctx.current_coupon_id is None:
        return

    await handler(RevokeCouponCmd(id=ctx.current_coupon_id))
