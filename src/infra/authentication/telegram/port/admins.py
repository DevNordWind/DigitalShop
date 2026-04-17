from typing import Protocol

from infra.authentication.telegram.model import TelegramId


class SuperAdminsProvider(Protocol):
    async def get(self) -> set[TelegramId]:
        raise NotImplementedError
