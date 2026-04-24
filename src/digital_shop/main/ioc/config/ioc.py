from adaptix import Retort
from config import Configuration
from config.bot import BotConfig
from config.db import DatabaseConfig
from config.file import FileStorageConfig
from config.log import LoggingConfig
from config.payment import PaymentConfig
from config.redis import RedisConfig
from dishka import Provider, Scope, provide


class ConfigurationProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_config(self, retort: Retort) -> Configuration:
        return Configuration.from_yaml(retort=retort)

    @provide
    async def get_bot_config(self, config: Configuration) -> BotConfig:
        return config.bot

    @provide
    async def get_db_config(self, config: Configuration) -> DatabaseConfig:
        return config.db

    @provide
    async def get_redis_config(self, config: Configuration) -> RedisConfig:
        return config.redis

    @provide
    async def get_log(self, config: Configuration) -> LoggingConfig:
        return config.log

    @provide
    async def get_file_config(
        self,
        config: Configuration,
    ) -> FileStorageConfig:
        return config.file

    @provide
    async def get_payment_config(self, config: Configuration) -> PaymentConfig:
        return config.payment
