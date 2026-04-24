from dataclasses import dataclass

from domain.common.localized import LocalizedTextError


class PositionDescriptionError(LocalizedTextError): ...


@dataclass
class PositionDescriptionTooShort(PositionDescriptionError):
    min_length: int


@dataclass
class PositionDescriptionTooLong(PositionDescriptionError):
    max_length: int
