from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Group, Select

from domain.common.money import Currency
from presentation.aiogram.dialog.user.profile.referral.create.callable import (
    on_select_currency,
)
from presentation.aiogram.dialog.user.profile.referral.create.getter import (
    select_currency_getter,
)
from presentation.aiogram.state import CreateReferrerProfileState
from presentation.aiogram.widget import GetText, GetTextSelect

select_currency = Window(
    GetText("referral-create-profile-currency"),
    Group(
        Select(
            GetTextSelect("referral-create-profile-currency.btn"),
            id="select_currency",
            on_click=on_select_currency,  # type: ignore[arg-type]
            items="buttons",
            type_factory=Currency,
            item_id_getter=lambda item: item.currency,
        ),
        width=2,
    ),
    Cancel(GetText("inl-ui.back")),
    state=CreateReferrerProfileState.select_currency,
    getter=select_currency_getter,
)
