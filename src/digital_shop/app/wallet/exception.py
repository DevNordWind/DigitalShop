from app.common.exception import ApplicationError


class WalletApplicationError(ApplicationError): ...


class WalletNotFound(WalletApplicationError): ...
