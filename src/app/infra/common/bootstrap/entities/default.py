from typing import Final

from app.domain.common.localized import Language
from app.domain.common.money import Currency
from app.domain.payment.enums import PaymentMethod
from app.presentation.aiogram.setting.category.model import CategorySettings
from app.presentation.aiogram.setting.general.model import (
    GeneralBotSettings,
    TechWorkSettings,
)
from app.presentation.aiogram.setting.payment.model import PaymentSettings
from app.presentation.aiogram.setting.position.model import PositionSettings

GENERAL_SETTINGS: Final[GeneralBotSettings] = GeneralBotSettings(
    tech_work=TechWorkSettings(status=True), support=None
)

CATEGORY_SETTINGS: Final[CategorySettings] = CategorySettings(
    default_lang=Language.RU, show_with_no_items=False
)

POSITION_SETTINGS: Final[PositionSettings] = PositionSettings(
    default_lang=Language.RU,
    default_currency=Currency.RUB,
    show_with_no_items=False,
)


def make_payment_settings(method: PaymentMethod) -> PaymentSettings:
    return PaymentSettings(method=method, is_active=False)
