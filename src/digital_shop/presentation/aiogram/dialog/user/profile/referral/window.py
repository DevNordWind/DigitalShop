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
from domain.common.money import Currency
from presentation.aiogram.dialog.user.profile.referral.callable import (
    on_change_currency,
    on_select_award,
    on_select_time_unit,
    on_sorting_order,
    on_switch_send_notifications,
)
from presentation.aiogram.dialog.user.profile.referral.ctx import (
    AWARDS_SCROLL,
    TimeUnit,
)
from presentation.aiogram.dialog.user.profile.referral.getter import (
    change_currency_getter,
    my_award_getter,
    my_awards_getter,
    referral_getter,
)
from presentation.aiogram.state import (
    CreateReferrerProfileState,
    ReferralState,
)
from presentation.aiogram.widget import GetText, GetTextSelect, Pagination


def map_unit(unit: str) -> TimeUnit | None:
    if unit == "None":
        return None

    return TimeUnit(unit)


referral = Window(
    GetText("referral"),
    Group(
        Select(
            GetTextSelect("referral.time-unit-btn"),
            id="select_unit",
            items="buttons",
            item_id_getter=lambda item: item.unit,
            type_factory=map_unit,
            on_click=on_select_time_unit,  # type: ignore[arg-type]
        ),
        width=2,
        when=F["is_referrer"],
    ),
    SwitchTo(
        GetText("referral.my-awards-btn"),
        id="to_my_awards",
        state=ReferralState.my_awards,
        when=F["is_referrer"],
    ),
    SwitchTo(
        GetText("referral.change-currency-btn"),
        id="to_change_currency",
        state=ReferralState.change_currency,
        when=F["is_referrer"],
    ),
    Button(
        GetText("referral.notifications-btn"),
        id="switch_notifications",
        on_click=on_switch_send_notifications,
        when=F["is_referrer"],
    ),
    Start(
        GetText("referral.get-link-btn"),
        id="to_create_profile",
        state=CreateReferrerProfileState.select_currency,
        when=~F["is_referrer"],
    ),
    Cancel(
        GetText("inl-ui.back"),
    ),
    state=ReferralState.referral,
    getter=referral_getter,
)

change_currency = Window(
    GetText("referral-change-currency"),
    Group(
        Select(
            GetTextSelect("referral-change-currency.btn"),
            id="select_currency",
            on_click=on_change_currency,  # type: ignore[arg-type]
            type_factory=Currency,
            items="buttons",
            item_id_getter=lambda item: item.currency,
        ),
        width=2,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=ReferralState.referral),
    state=ReferralState.change_currency,
    getter=change_currency_getter,
)

my_awards = Window(
    GetText("referral-my-awards"),
    Button(
        GetText("referral-my-awards.order-btn"),
        id="sorting_order",
        on_click=on_sorting_order,
    ),
    Group(
        Select(
            GetTextSelect("referral-my-awards.btn"),
            id="s_a",
            type_factory=UUID,
            items="buttons",
            item_id_getter=lambda item: item.id,
            on_click=on_select_award,  # type: ignore[arg-type]
        ),
        width=1,
    ),
    Pagination(scroll_id=AWARDS_SCROLL),
    SwitchTo(GetText("inl-ui.back"), id="back", state=ReferralState.referral),
    state=ReferralState.my_awards,
    getter=my_awards_getter,
)

my_award = Window(
    GetText("referral-my-award"),
    SwitchTo(GetText("inl-ui.back"), id="back", state=ReferralState.my_awards),
    state=ReferralState.my_award,
    getter=my_award_getter,
)
