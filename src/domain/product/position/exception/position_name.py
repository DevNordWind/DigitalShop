from dataclasses import dataclass

from domain.common.localized import LocalizedTextError


class PositionNameError(LocalizedTextError): ...


@dataclass
class PositionNameTooShort(PositionNameError):
    min_length: int


@dataclass
class PositionNameTooLong(PositionNameError):
    max_length: int
