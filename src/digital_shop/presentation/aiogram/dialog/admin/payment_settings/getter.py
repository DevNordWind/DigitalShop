from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from app.payment.query import GetPaymentCommission, GetPaymentCommissionQuery
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.payment.enums import CommissionType, PaymentMethod
from presentation.aiogram.dialog.admin.payment_settings.ctx import (
    CTX_KEY,
    PaymentSettingsCtx,
)
from presentation.aiogram.setting.payment.port import (
    PaymentSettingsGateway,
)


@dataclass(slots=True, frozen=True)
class PaymentMethodButton:
    method: PaymentMethod


@dataclass(slots=True, frozen=True)
class CommissionButton:
    type: CommissionType

    is_current: bool


async def select_method_getter(
    **_: Any,
) -> dict[str, Any]:
    return {
        "buttons": [
            PaymentMethodButton(method=method) for method in PaymentMethod
        ],
    }


@inject
async def setting_getter(
    dialog_manager: DialogManager,
    gateway: FromDishka[PaymentSettingsGateway],
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetPaymentCommission],
    **_: Any,
) -> dict[str, Any]:
    ctx: PaymentSettingsCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PaymentSettingsCtx,
    )
    if ctx.current_method is None:
        return {}
    settings = await gateway.get_by_method(method=ctx.current_method)

    commission = await query_handler(
        GetPaymentCommissionQuery(method=ctx.current_method),
    )

    return {
        "commission_percent": commission.coefficient.as_percent
        if commission.coefficient
        else None,
        "method": ctx.current_method,
        "buttons": [
            CommissionButton(type=tp, is_current=commission.type == tp)
            for tp in CommissionType
        ],
        "is_active": settings.is_active,
    }
