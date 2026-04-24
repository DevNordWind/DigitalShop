from dataclasses import dataclass
from urllib.parse import quote


@dataclass(frozen=True, slots=True)
class RedisConfig:
    db: int
    host: str
    port: int
    password: None | str
    username: None | str

    @property
    def url(self) -> str:
        auth: str = ""

        if self.username is not None:
            auth += quote(self.username)

        if self.password is not None:
            auth += f":{quote(self.password)}"

        if auth:
            auth += "@"

        return f"redis://{auth}{self.host}:{self.port}/{self.db}"
