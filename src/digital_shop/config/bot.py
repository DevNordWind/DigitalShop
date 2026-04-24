from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BotConfig:
    token: str
    super_admins: list[int]

    webhook: BotWebhookConfig | None


@dataclass(frozen=True, slots=True)
class BotWebhookConfig:
    base_url: str
    secret: str | None
    with_ip_filter: bool
    path: str = "/webhoks/bots"

    @property
    def url(self) -> str:
        return self.base_url + self.path

    def __post_init__(self) -> None:
        object.__setattr__(self, "base_url", self.base_url.rstrip("/"))
