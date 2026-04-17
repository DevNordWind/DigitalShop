from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.referral.cmd import CreateReferrerProfile, CreateReferrerProfileCmd
from domain.common.money import Currency


@inject
async def on_select_currency(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    handler: FromDishka[CreateReferrerProfile],
) -> None:
    await handler(
        CreateReferrerProfileCmd(
            award_currency=currency,
            send_notifications=True,
        ),
    )
    await dialog_manager.done()
