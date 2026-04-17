from aiogram.fsm.state import State, StatesGroup


class AdminRootState(StatesGroup):
    root = State()


class AdminCategoryState(StatesGroup):
    categories = State()
    category = State()
    filters = State()

    archive_confirmation = State()
    delete_confirmation = State()

    archive_all_confirmation = State()
    delete_all_confirmation = State()


class CreateCategoryState(StatesGroup):
    view = State()
    input_name = State()
    input_description = State()
    input_media = State()


class EditCategoryState(StatesGroup):
    edit_name = State()
    edit_name_default_lang = State()
    edit_description = State()
    edit_description_default_lang = State()
    edit_media = State()


class CategorySettingsState(StatesGroup):
    settings = State()
    default_lang = State()


class PaymentSettingsState(StatesGroup):
    select_method = State()
    setting = State()
    input_commission = State()


class AdminPositionState(StatesGroup):
    select_category = State()
    category_filters = State()
    select_position = State()
    position_filters = State()
    position = State()
    archive_confirmation = State()
    delete_confirmation = State()
    delete_all_confirmation = State()
    archive_all_confirmation = State()


class PositionSettingsState(StatesGroup):
    settings = State()
    filter = State()
    default_lang = State()
    default_currency = State()


class CreatePositionState(StatesGroup):
    view = State()
    input_name = State()
    input_description = State()
    input_price = State()
    input_media = State()
    select_warehouse = State()


class EditPositionState(StatesGroup):
    edit_name = State()
    edit_name_default_lang = State()
    edit_description = State()
    edit_description_default_lang = State()
    edit_price = State()
    edit_price_base_currency = State()
    edit_media = State()


class FixedItemState(StatesGroup):
    item = State()
    add = State()
    replace = State()
    archive = State()
    archived_item = State()

    archive_confirmation = State()
    delete_confirmation = State()


class StockItemState(StatesGroup):
    items = State()
    item = State()
    add = State()
    filters = State()

    archive_confirmation = State()
    delete_confirmation = State()

    archive_all_confirmation = State()
    delete_all_confirmation = State()


class AdminCouponState(StatesGroup):
    coupons = State()
    coupon = State()
    filters = State()


class CreateCouponState(StatesGroup):
    view = State()
    input_code = State()
    select_type = State()
    input_amount = State()
    input_percent = State()
    input_valid_from = State()
    input_valid_until = State()


class CreateUrlButtonState(StatesGroup):
    url_button = State()
    input_name = State()
    input_url = State()


class BroadcastState(StatesGroup):
    broadcast = State()
    preview_select_lang = State()

    preview = State()
    input_texts = State()
    input_media = State()
    buttons = State()


class UsersManagementState(StatesGroup):
    users = State()
    find = State()
    user = State()

    input_top_up_amount = State()


class GeneralSettingsState(StatesGroup):
    general_settings = State()
    input_referral_percent = State()
    input_support_contact = State()


class AdminStatisticState(StatesGroup):
    statistic = State()
    input_period = State()
    convert = State()
