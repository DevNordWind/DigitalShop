from dataclasses import dataclass

from app.domain.common.exception import ValueObjectError


class ItemContentError(ValueObjectError): ...


@dataclass
class ItemContentTooLongError(ItemContentError):
    max_length: int


@dataclass
class ItemContentTooShortError(ItemContentError):
    min_length: int
