from app.presentation.aiogram.exception import (
    TelegramBotSettingsBootstrapError,
    TelegramBotSettingsError,
    TelegramBotSettingsPermissionDeniedError,
)


class PositionSettingsError(TelegramBotSettingsError): ...


class PositionSettingsPermissionDeniedError(
    PositionSettingsError, TelegramBotSettingsPermissionDeniedError
): ...


class PositionSettingsNotCreatedError(
    PositionSettingsError, TelegramBotSettingsBootstrapError
): ...
