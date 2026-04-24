from aiogram_dialog import Dialog

from .callable import on_start
from .create import get_create_referrer_profile_dialog
from .window import change_currency, my_award, my_awards, referral


def get_referral_dialogs() -> tuple[Dialog, Dialog]:
    return (
        Dialog(
            change_currency,
            my_awards,
            my_award,
            referral,
            on_start=on_start,
        ),
        get_create_referrer_profile_dialog(),
    )
