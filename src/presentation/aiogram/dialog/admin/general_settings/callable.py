from decimal import Decimal

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from dishka import AsyncContainer, FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.coefficient import CoefficientDTO
from app.referral.cmd import SetReferralCoefficient, SetReferralCoefficientCmd
from presentation.aiogram.setting.general.handler import (
    SetSupportUsername,
    SetSupportUsernameCmd,
    SwitchTechWorkStatus,
)
from presentation.aiogram.state.admin import GeneralSettingsState


@inject
async def on_switch_tech_work_status(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[SwitchTechWorkStatus],
    container: FromDishka[AsyncContainer],
) -> None:
    await handler.execute()
    await container.close()


@inject
async def on_input_support_contact(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    contact: str,
    handler: FromDishka[SetSupportUsername],
    container: FromDishka[AsyncContainer],
) -> None:
    await handler.execute(SetSupportUsernameCmd(username=contact))
    await container.close()
    await event.delete()

    await dialog_manager.switch_to(
        state=GeneralSettingsState.general_settings, show_mode=ShowMode.EDIT
    )


@inject
async def on_input_referral_percent(
    event: Message,
    widget: ManagedTextInput[Decimal],
    dialog_manager: DialogManager,
    percent: Decimal,
    handler: FromDishka[SetReferralCoefficient],
    container: FromDishka[AsyncContainer],
) -> None:
    await handler(
        SetReferralCoefficientCmd(
            coefficient=CoefficientDTO.from_percent(percent=percent)
        )
    )
    await container.close()
    await event.delete()
    await dialog_manager.switch_to(state=GeneralSettingsState.general_settings)
