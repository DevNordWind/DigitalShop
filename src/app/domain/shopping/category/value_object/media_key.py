from dataclasses import dataclass

from app.domain.common.file_key import FileKey
from app.domain.shopping.category.exception import (
    CategoryMediaKeyMustBeMediaError,
)


@dataclass(slots=True, frozen=True)
class CategoryMediaKey(FileKey):
    def __post_init__(self) -> None:
        if not self.is_media:
            raise CategoryMediaKeyMustBeMediaError

        FileKey.__post_init__(self)
