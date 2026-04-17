from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Start

from domain.user.enums import UserRole
from presentation.aiogram.state import (
    AdminRootState,
    InfoState,
    ProfileState,
    RootState,
    ShoppingState,
    WalletState,
)
from presentation.aiogram.widget import GetText

from .getter import root_getter

root: Window = Window(
    GetText("root"),
    Start(
        GetText("root.buy-btn"),
        id="to_product",
        state=ShoppingState.select_category,
    ),
    Group(
        Start(
            GetText(
                "root.profile-btn",
            ),
            id="to_profile",
            state=ProfileState.profile,
        ),
        Start(GetText("root.info-btn"), id="to_info", state=InfoState.info),
        width=2,
    ),
    Start(
        GetText("root.wallet-btn"),
        id="to_wallet",
        state=WalletState.wallet,
    ),
    Start(
        GetText("root.admin-panel-btn"),
        when=F["user_role"] >= UserRole.ADMIN,
        id="to_admin_root",
        state=AdminRootState.root,
    ),
    getter=root_getter,
    state=RootState.root,
)
