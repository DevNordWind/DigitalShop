from collections.abc import Sequence
from typing import Protocol


class DatabaseSession(Protocol):
    async def commit(self) -> None: ...

    async def flush(self, objects: Sequence[object] | None = None) -> None: ...

    async def rollback(self) -> None: ...
