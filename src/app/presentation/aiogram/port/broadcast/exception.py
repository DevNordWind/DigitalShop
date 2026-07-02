from app.presentation.aiogram.exception import TelegramBotValidationError


class BroadcastRequestError(TelegramBotValidationError): ...


class BroadcastTextsAsymmetricallyError(BroadcastRequestError): ...
