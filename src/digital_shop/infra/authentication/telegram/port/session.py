from typing import Protocol


class NonExpiringSession(Protocol):
    async def commit(self) -> None:
        raise NotImplementedError

    @property
    def dirty(self) -> bool:
        raise NotImplementedError
