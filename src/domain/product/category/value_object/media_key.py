from dataclasses import dataclass

from domain.common.file import FileKey
from domain.product.category.exception import (
    CategoryMediaKeyMustBeMediaError,
)


@dataclass(slots=True, frozen=True)
class CategoryMediaKey(FileKey):
    def __post_init__(self) -> None:
        if not self.is_media:
            raise CategoryMediaKeyMustBeMediaError

        FileKey.__post_init__(self)
