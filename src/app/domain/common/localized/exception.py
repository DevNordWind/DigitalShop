from dataclasses import dataclass

from app.domain.common.exception import DomainRuleViolationError, ValueObjectError
from app.domain.common.localized import Language


class LocalizedTextError(ValueObjectError): ...


@dataclass
class DefaultLanguageMissingError(LocalizedTextError, DomainRuleViolationError):
    lang: Language


class DefaultLanguageDeletionForbiddenError(
    LocalizedTextError, DomainRuleViolationError
): ...
