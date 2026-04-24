from decimal import Decimal
from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from app.common.dto.coefficient import CoefficientDTO
from app.payment.cmd import (
    ChangePaymentCommissionCoefficient,
    ChangePaymentCommissionCoefficientCmd,
)
from app.payment.dto.commission import CommissionDTO
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.payment.enums import CommissionType, PaymentMethod
from presentation.aiogram.dialog.admin.payment_settings.ctx import (
    CTX_KEY,
    PaymentSettingsCtx,
)
from presentation.aiogram.setting.payment.cmd import (
    SwitchPaymentSettingStatus,
    SwitchPaymentSettingStatusCmd,
)
from presentation.aiogram.state.admin import PaymentSettingsState


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = PaymentSettingsCtx()
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_payment_method(
    event: CallbackQuery,
    widget: Select[PaymentMethod],
    dialog_manager: DialogManager,
    method: PaymentMethod,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], PaymentSettingsCtx)
    ctx.current_method = method

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(state=PaymentSettingsState.setting)


@inject
async def on_change_commission(
    event: CallbackQuery,
    widget: Select[CommissionType],
    dialog_manager: DialogManager,
    tp: CommissionType,
    handler: FromDishka[ChangePaymentCommissionCoefficient],
    retort: FromDishka[Retort],
) -> None:
    ctx: PaymentSettingsCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PaymentSettingsCtx,
    )
    if ctx.current_method is None:
        return None

    if tp == CommissionType.SHOP:
        return await handler(
            cmd=ChangePaymentCommissionCoefficientCmd(
                method=ctx.current_method,
                new_commission=CommissionDTO(type=tp, coefficient=None),
            ),
        )
    return await dialog_manager.switch_to(
        state=PaymentSettingsState.input_commission,
    )


@inject
async def on_switch_status(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[SwitchPaymentSettingStatus],
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], PaymentSettingsCtx)
    if ctx.current_method is None:
        return None

    return await handler(
        SwitchPaymentSettingStatusCmd(
            method=PaymentMethod(ctx.current_method)
        ),
    )


@inject
async def on_input_commission(
    event: Message,
    widget: ManagedTextInput[Decimal],
    dialog_manager: DialogManager,
    percent: Decimal,
    handler: FromDishka[ChangePaymentCommissionCoefficient],
    retort: FromDishka[Retort],
) -> None:
    ctx: PaymentSettingsCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PaymentSettingsCtx,
    )
    if ctx.current_method is None:
        return

    await handler(
        ChangePaymentCommissionCoefficientCmd(
            method=ctx.current_method,
            new_commission=CommissionDTO(
                type=CommissionType.CUSTOMER,
                coefficient=CoefficientDTO(percent / Decimal("100.00")),
            ),
        ),
    )
    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT
    await dialog_manager.switch_to(state=PaymentSettingsState.setting)
