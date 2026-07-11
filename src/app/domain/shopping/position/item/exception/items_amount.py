from app.domain.common.exception import ValueObjectError


class ItemsAmountError(ValueObjectError): ...


class NegativeItemsAmountForbiddenError(ItemsAmountError): ...
