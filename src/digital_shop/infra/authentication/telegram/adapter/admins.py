from config.bot import BotConfig
from infra.authentication.telegram.model import TelegramId
from infra.authentication.telegram.port import SuperAdminsProvider


class DefaultSuperAdminsProvider(SuperAdminsProvider):
    def __init__(self, config: BotConfig):
        self._config: BotConfig = config

    async def get(self) -> set[TelegramId]:
        return {TelegramId(id_) for id_ in self._config.super_admins}
