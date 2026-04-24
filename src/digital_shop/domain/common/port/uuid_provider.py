from typing import Protocol
from uuid import UUID


class UUIDProvider(Protocol):
    def __call__(self) -> UUID: ...
