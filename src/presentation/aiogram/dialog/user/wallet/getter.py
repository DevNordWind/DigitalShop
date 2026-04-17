from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.query_params import SortingOrder
from app.wallet.dto.sorting import WalletSortingParams
from app.wallet.query import GetMyWalletsWithTotal
from app.wallet.query.get_my_with_total import (
    GetMyWalletsWithTotalQuery,
    WalletsWithTotal,
)
from domain.common.money import Currency
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.user.wallet.ctx import CTX_KEY, WalletCtx
from presentation.aiogram.port import Text


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


@inject
async def wallet_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetMyWalletsWithTotal],
    tg_ctx: FromDishka[TelegramContextDTO],
    text: FromDishka[Text],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: WalletCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        WalletCtx,
    )

    dto: WalletsWithTotal = await query_handler(
        query=GetMyWalletsWithTotalQuery(
            sorting=WalletSortingParams(
                field="currency",
                order=SortingOrder.DESC,
            ),
            target_total=tg_ctx.currency,
        ),
    )
    rows: list[str] = []
    amount: Decimal = Decimal("0.00")

    for wallet in sorted(
        dto.wallets,
        key=lambda x: x.currency != tg_ctx.currency,
    ):
        if wallet.currency == tg_ctx.currency:
            amount = wallet.balance.amount

        rows.append(
            text(
                "wallet-row-selector",
                is_current=wallet.currency == tg_ctx.currency,
                currency=wallet.currency,
                amount=wallet.balance.amount,
            ),
        )

    return {
        "rows": "\n".join(rows),
        "total": dto.total.amount,
        "currency": tg_ctx.currency,
        "show_all": ctx.show_all_balances,
        "amount": amount,
    }


@inject
async def change_wallet_getter(
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    return {
        "buttons": [
            CurrencyButton(
                currency=currency, is_current=currency == tg_ctx.currency
            )
            for currency in Currency
        ]
    }
