from app.presentation.aiogram.exception import (
    TelegramBotSettingsBootstrapError,
    TelegramBotSettingsError,
    TelegramBotSettingsPermissionDeniedError,
)


class GeneralBotSettingsError(TelegramBotSettingsError): ...


class GeneralBotSettingsPermissionDeniedError(
    GeneralBotSettingsError, TelegramBotSettingsPermissionDeniedError
): ...


class GeneralSettingsNotCreatedError(
    GeneralBotSettingsError, TelegramBotSettingsBootstrapError
): ...


class CannotExcludeTechWorkForUsersError(GeneralBotSettingsError): ...
