from dataclasses import dataclass

from app.domain.common.localized import LocalizedTextError


class PositionDescriptionError(LocalizedTextError): ...


@dataclass
class PositionDescriptionTooShortError(PositionDescriptionError):
    min_length: int


@dataclass
class PositionDescriptionTooLongError(PositionDescriptionError):
    max_length: int
