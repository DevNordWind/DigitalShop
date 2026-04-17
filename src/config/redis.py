from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RedisConfig:
    db: int
    host: str
    port: int
    password: None | str
    username: None | str
