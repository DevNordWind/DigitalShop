from decimal import Decimal

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Data, DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.money import MoneyDTO
from app.user.cmd import AssignUserRole, AssignUserRoleCmd
from app.user.dto.report import UserProfileReport
from app.user.query import GetUserProfileReport, GetUserProfileReportQuery
from app.wallet.cmd import TopUpWalletManually, TopUpWalletManuallyCmd
from domain.common.money import Currency
from domain.user.enums import UserRole
from presentation.aiogram.dialog.admin.users_management.ctx import (
    CTX_KEY,
    UsersManagementCtx,
)
from presentation.aiogram.port import Text
from presentation.aiogram.state import OrdersState, UsersManagementState


@inject
async def on_start(
    _: Data, dialog_manager: DialogManager, retort: FromDishka[Retort]
) -> None:
    ctx = UsersManagementCtx()
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_user_identifier(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    identifier: str,
    retort: FromDishka[Retort],
    handler: FromDishka[GetUserProfileReport],
) -> None:
    profile: UserProfileReport = await handler(
        GetUserProfileReportQuery(target_identifier=identifier)
    )
    await event.delete()
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], UsersManagementCtx)
    ctx.current_user_id = profile.id

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(state=UsersManagementState.user, show_mode=ShowMode.EDIT)


@inject
async def on_promote_to_admin(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[AssignUserRole],
    retort: FromDishka[Retort],
) -> None:
    ctx: UsersManagementCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UsersManagementCtx
    )
    if ctx.current_user_id is None:
        return

    await handler(
        AssignUserRoleCmd(
            target_user_id=ctx.current_user_id, target_role=UserRole.ADMIN
        )
    )


@inject
async def on_demote_to_user(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[AssignUserRole],
    retort: FromDishka[Retort],
) -> None:
    ctx: UsersManagementCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UsersManagementCtx
    )
    if ctx.current_user_id is None:
        return

    await handler(
        AssignUserRoleCmd(
            target_user_id=ctx.current_user_id, target_role=UserRole.USER
        )
    )


@inject
async def on_select_top_up_currency(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    retort: FromDishka[Retort],
) -> None:
    ctx: UsersManagementCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UsersManagementCtx
    )
    ctx.current_top_up_currency = currency
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_top_amount(
    event: Message,
    widget: ManagedTextInput[Decimal],
    dialog_manager: DialogManager,
    amount: Decimal,
    retort: FromDishka[Retort],
    handler: FromDishka[TopUpWalletManually],
    t: FromDishka[Text],
) -> Message | None:
    ctx: UsersManagementCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UsersManagementCtx
    )
    if ctx.current_user_id is None:
        return None

    if ctx.current_top_up_currency is None:
        return await event.reply(
            t("users-management-top-up.unselected-currency")
        )

    await handler(
        TopUpWalletManuallyCmd(
            amount=MoneyDTO(
                amount=amount, currency=ctx.current_top_up_currency
            ),
            target_user_id=ctx.current_user_id,
        )
    )
    await event.delete()
    await dialog_manager.switch_to(
        state=UsersManagementState.user, show_mode=ShowMode.EDIT
    )
    return None


@inject
async def on_start_orders(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: UsersManagementCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UsersManagementCtx
    )
    if ctx.current_user_id is None:
        return

    await dialog_manager.start(
        state=OrdersState.orders, data={"current_user_id": ctx.current_user_id}
    )
