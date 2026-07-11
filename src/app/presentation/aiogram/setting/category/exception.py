from app.presentation.aiogram.exception import (
    TelegramBotSettingsBootstrapError,
    TelegramBotSettingsError,
    TelegramBotSettingsPermissionDeniedError,
)


class CategorySettingsError(TelegramBotSettingsError): ...


class CategorySettingsPermissionDeniedError(
    CategorySettingsError, TelegramBotSettingsPermissionDeniedError
): ...


class CategorySettingsNotCreatedError(
    CategorySettingsError, TelegramBotSettingsBootstrapError
): ...
