from app.app.common.exception import AppError


class UserAppError(AppError): ...


class UserAuthenticationError(UserAppError): ...
