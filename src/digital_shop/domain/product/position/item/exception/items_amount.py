from domain.common.exception import ValueObjectError


class ItemsAmountError(ValueObjectError): ...


class NegativeItemsAmountError(ItemsAmountError): ...
