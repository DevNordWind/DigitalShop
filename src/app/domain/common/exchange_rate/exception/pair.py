from app.domain.common.exception import ValueObjectError


class CurrencyPairError(ValueObjectError): ...


class CurrencyPairSameCurrencyError(CurrencyPairError): ...
