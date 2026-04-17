from uuid import UUID

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    Start,
    SwitchTo,
)

from domain.coupon.enums import CouponStatus
from presentation.aiogram.state import AdminCouponState, CreateCouponState
from presentation.aiogram.widget import GetText, GetTextSelect, Pagination

from .callable import (
    on_coupon_status,
    on_revoke,
    on_select_coupon,
    on_sorting_order,
)
from .ctx import COUPONS_SCROLL
from .getter import coupon_getter, coupons_getter, filters_getter

coupons = Window(
    GetText("admin-coupons"),
    SwitchTo(
        GetText("admin-coupons.filters"),
        id="to_filter",
        state=AdminCouponState.filters,
    ),
    Group(
        Select(
            GetTextSelect("admin-coupons.btn"),
            id="s_c",
            type_factory=UUID,
            items="buttons",
            item_id_getter=lambda item: item.id,
            on_click=on_select_coupon,  # type: ignore[arg-type]
        ),
        width=1,
    ),
    Start(
        GetText("inl-ui.create"),
        id="to_create",
        state=CreateCouponState.view,
    ),
    Pagination(scroll_id=COUPONS_SCROLL),
    Cancel(GetText("inl-ui.back")),
    state=AdminCouponState.coupons,
    getter=coupons_getter,
)

filters = Window(
    GetText("admin-coupons-filters"),
    Button(
        GetText("admin-coupons-filters.order-btn"),
        id="order",
        on_click=on_sorting_order,
    ),
    Group(
        Select(
            GetTextSelect("admin-coupons-filters.status-btn"),
            id="select_status",
            type_factory=CouponStatus,
            items="buttons",
            on_click=on_coupon_status,  # type: ignore[arg-type]
            item_id_getter=lambda item: item.status,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminCouponState.coupons,
    ),
    getter=filters_getter,
    state=AdminCouponState.filters,
)

coupon = Window(
    GetText("admin-coupon"),
    Button(
        GetText("admin-coupon.revoke-btn"),
        id="revoke",
        on_click=on_revoke,
        when=~F["is_revoked"],
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminCouponState.coupons,
    ),
    state=AdminCouponState.coupon,
    getter=coupon_getter,
)
