from domain.common.exception import ValueObjectError


class CurrencyPairError(ValueObjectError): ...


class CurrencyPairSameCurrency(CurrencyPairError): ...
