from typing import Final

from domain.common.localized import Language
from domain.common.money import Currency
from domain.payment.enums import PaymentMethod
from presentation.aiogram.setting.category.model import CategorySettings
from presentation.aiogram.setting.general.model import (
    GeneralBotSettings,
    TechWorkSettings,
)
from presentation.aiogram.setting.payment.model import PaymentSettings
from presentation.aiogram.setting.position.model import PositionSettings

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

PAYMENT_SETTINGS: tuple[PaymentSettings, ...] = tuple(
    PaymentSettings(method=method, is_active=False) for method in PaymentMethod
)
