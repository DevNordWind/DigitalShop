from dataclasses import dataclass

from app.domain.common.localized import LocalizedTextError


class PositionNameError(LocalizedTextError): ...


@dataclass
class PositionNameTooShortError(PositionNameError):
    min_length: int


@dataclass
class PositionNameTooLongError(PositionNameError):
    max_length: int
