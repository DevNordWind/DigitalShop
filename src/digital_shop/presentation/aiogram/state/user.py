from aiogram.fsm.state import State, StatesGroup


class WalletState(StatesGroup):
    wallet = State()
    change_wallet = State()


class CurrencyRatesState(StatesGroup):
    rates = State()
    related_rates = State()


class InfoState(StatesGroup):
    info = State()


class TopUpState(StatesGroup):
    input_amount = State()
    select_payment_method = State()
    select_currency = State()
    payment = State()


class ShoppingState(StatesGroup):
    select_category = State()
    select_position = State()
    position = State()

    input_items_amount = State()


class OrderState(StatesGroup):
    order = State()
    input_coupon_code = State()
    select_payment_method = State()
    input_new_items_amount = State()

    payment = State()


class ReferralState(StatesGroup):
    referral = State()
    my_awards = State()
    my_award = State()
    change_currency = State()


class CreateReferrerProfileState(StatesGroup):
    select_currency = State()


class ProfileState(StatesGroup):
    profile = State()


class LanguageState(StatesGroup):
    select_lang = State()


class OrdersState(StatesGroup):
    orders = State()
    filters = State()
    order = State()
