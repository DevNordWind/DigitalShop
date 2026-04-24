from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Group, Start
from presentation.aiogram.state import (
    AdminCategoryState,
    AdminCouponState,
    AdminPositionState,
    AdminRootState,
    AdminStatisticState,
    UsersManagementState,
)
from presentation.aiogram.state.admin import (
    GeneralSettingsState,
    PaymentSettingsState,
)
from presentation.aiogram.widget import GetText

root = Window(
    GetText("admin-root"),
    Group(
        Start(
            GetText("admin-root.categories-btn"),
            id="start_categories",
            state=AdminCategoryState.categories,
        ),
        Start(
            GetText("admin-root.positions-btn"),
            id="start_positions",
            state=AdminPositionState.select_category,
        ),
        width=2,
    ),
    Start(
        GetText("admin-root.statistic-btn"),
        id="start_statistic",
        state=AdminStatisticState.statistic,
    ),
    Start(
        GetText("admin-root.coupons-btn"),
        id="start_coupons",
        state=AdminCouponState.coupons,
    ),
    Start(
        GetText("admin-root.users-management-btn"),
        id="start_users_management",
        state=UsersManagementState.users,
    ),
    Start(
        GetText("admin-root.settings-btn"),
        id="start_settings",
        state=GeneralSettingsState.general_settings,
    ),
    Start(
        GetText("admin-root.payment-settings-btn"),
        id="start_payment_settings",
        state=PaymentSettingsState.select_method,
    ),
    Cancel(
        GetText("inl-ui.back"),
    ),
    state=AdminRootState.root,
)
