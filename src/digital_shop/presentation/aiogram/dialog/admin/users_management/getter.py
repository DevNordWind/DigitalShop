from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from app.common.dto.query_params import SortingOrder
from app.user.dto.report import UserProfileReport
from app.user.query import GetUserProfileReport, GetUserProfileReportQuery
from app.wallet.dto.sorting import WalletSortingParams
from app.wallet.dto.wallet import WalletDTO
from app.wallet.query import ListWalletsByUserId, ListWalletsByUserIdQuery
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.money import Currency
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.port import Text

from .ctx import CTX_KEY, UsersManagementCtx


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


@inject
async def user_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetUserProfileReport],
    wallets_handler: FromDishka[ListWalletsByUserId],
    t: FromDishka[Text],
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    ctx: UsersManagementCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UsersManagementCtx
    )
    if ctx.current_user_id is None:
        return {}

    profile: UserProfileReport = await query_handler(
        GetUserProfileReportQuery(target_identifier=ctx.current_user_id)
    )
    wallets: list[WalletDTO] = await wallets_handler(
        ListWalletsByUserIdQuery(
            user_id=profile.id,
            sorting=WalletSortingParams(
                field="currency", order=SortingOrder.DESC
            ),
        )
    )
    wallets_rows: list[str] = [
        t(
            "users-management-wallet-row",
            amount=wallet.balance.amount,
            currency=wallet.currency,
            is_last=len(wallets) == i,
        )
        for i, wallet in enumerate(wallets, start=1)
    ]

    return {
        "user_id": profile.id,
        "role": profile.role,
        "wallets_rows": "\n".join(wallets_rows),
        "orders_count": profile.orders_count,
        "top_ups_count": profile.top_ups_count,
        "reg_at": profile.reg_at,
        "user_role": tg_ctx.user_role,
    }


@inject
async def input_top_up_amount_getter(
    dialog_manager: DialogManager, retort: FromDishka[Retort], **_: Any
) -> dict[str, Any]:
    ctx: UsersManagementCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UsersManagementCtx
    )
    return {
        "buttons": [
            CurrencyButton(
                currency=currency,
                is_current=ctx.current_top_up_currency == currency,
            )
            for currency in Currency
        ]
    }
