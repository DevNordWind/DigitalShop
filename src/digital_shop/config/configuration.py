import pathlib
from dataclasses import dataclass

import yaml
from adaptix import Retort
from config.bot import BotConfig
from config.db import DatabaseConfig
from config.file import FileStorageConfig
from config.log import LoggingConfig
from config.payment import PaymentConfig
from config.redis import RedisConfig


@dataclass(frozen=True, slots=True)
class Configuration:
    bot: BotConfig
    db: DatabaseConfig
    redis: RedisConfig
    file: FileStorageConfig
    payment: PaymentConfig
    log: LoggingConfig

    @classmethod
    def from_yaml(
        cls,
        retort: Retort,
        path: str = "./config.yaml",
    ) -> Configuration:
        with pathlib.Path(path).open() as config_file:
            raw = yaml.safe_load(config_file)
        return cls(
            bot=retort.load(raw["bot"], BotConfig),
            log=retort.load(raw["log"], LoggingConfig),
            db=retort.load(raw["postgres"], DatabaseConfig),
            redis=retort.load(raw["redis"], RedisConfig),
            payment=retort.load(raw["payment"], PaymentConfig),
            file=retort.load(raw["file_storage"], FileStorageConfig),
        )
