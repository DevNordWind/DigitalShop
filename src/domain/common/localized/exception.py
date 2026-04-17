from dataclasses import dataclass

from domain.common.exception import ValueObjectError
from domain.common.localized import Language


class LocalizedTextError(ValueObjectError): ...


@dataclass
class DefaultLanguageMissingError(LocalizedTextError):
    lang: Language


class CannotRemoveDefaultLanguage(LocalizedTextError): ...
