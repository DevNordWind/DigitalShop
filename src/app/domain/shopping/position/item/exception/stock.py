from app.domain.common.exception import (
    DomainRuleViolationError,
)
from app.domain.shopping.position.exception import (
    PositionItemError,
    PositionItemNotFoundError,
)


class StockItemError(PositionItemError): ...


class StockItemArchivationForbiddenError(StockItemError, DomainRuleViolationError): ...


class StockItemNotFoundError(StockItemError, PositionItemNotFoundError): ...


class StockItemContentReplacingForbiddenError(
    StockItemError, DomainRuleViolationError
): ...


class StockItemRecoverForbiddenError(StockItemError, DomainRuleViolationError): ...


class StockItemReservationForbiddenError(StockItemError, DomainRuleViolationError): ...


class StockItemSellForbiddenError(StockItemError, DomainRuleViolationError): ...


class StockItemReleaseForbiddenError(StockItemError, DomainRuleViolationError): ...


class StockItemDeletionForbiddenError(StockItemError, DomainRuleViolationError): ...
