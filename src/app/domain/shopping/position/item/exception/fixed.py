from app.domain.common.exception import (
    DomainRuleViolationError,
)
from app.domain.shopping.position.exception import (
    PositionItemError,
    PositionItemNotFoundError,
)


class FixedItemError(PositionItemError): ...


class FixedItemNotFoundError(FixedItemError, PositionItemNotFoundError): ...


class FixedItemContentReplacingForbiddenError(
    FixedItemError, DomainRuleViolationError
): ...


class FixedItemDeletionForbiddenError(FixedItemError, DomainRuleViolationError): ...


class FixedItemArchivationForbiddenError(FixedItemError, DomainRuleViolationError): ...


class FixedItemRecoverForbiddenError(FixedItemError, DomainRuleViolationError): ...
