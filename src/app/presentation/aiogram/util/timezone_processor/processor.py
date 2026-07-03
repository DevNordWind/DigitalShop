from datetime import datetime

from app.infra.authentication.telegram.dto import TelegramContextDTO


class TimeZoneProcessor:
    def __init__(self, ctx: TelegramContextDTO):
        self._ctx = ctx

    def process(self, dt: datetime) -> datetime:
        if not isinstance(dt, datetime):
            raise TypeError

        return dt.astimezone(tz=self._ctx.timezone)
