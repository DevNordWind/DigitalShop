from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OffsetPaginationParams:
    limit: int
    offset: int

    def __post_init__(self) -> None:
        if self.limit <= 0:
            object.__setattr__(self, "limit", 10)
        if self.offset < 0:
            object.__setattr__(self, "offset", 0)
