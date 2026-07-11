from app.presentation.aiogram.exception import (
    TelegramBotSettingsBootstrapError,
    TelegramBotSettingsError,
    TelegramBotSettingsPermissionDeniedError,
)


class PaymentSettingsError(TelegramBotSettingsError): ...


class PaymentSettingsNotCreatedError(
    PaymentSettingsError, TelegramBotSettingsBootstrapError
): ...


class PaymentSettingsPermissionDeniedError(
    PaymentSettingsError, TelegramBotSettingsPermissionDeniedError
): ...
