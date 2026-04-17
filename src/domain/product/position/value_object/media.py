from dataclasses import dataclass

from domain.common.file import FileKey
from domain.product.position.exception import (
    PositionMediaKeyMustBeMediaError,
)


@dataclass(slots=True, frozen=True)
class PositionMediaKey(FileKey):
    def __post_init__(self) -> None:
        if not self.is_media:
            raise PositionMediaKeyMustBeMediaError

        FileKey.__post_init__(self)
