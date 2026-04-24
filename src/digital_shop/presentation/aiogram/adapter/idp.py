from app.user.port import UserIdentifyProvider
from domain.user.enums import UserRole
from domain.user.value_object import UserId
from infra.authentication.telegram.dto import TelegramContextDTO


class AiogramUserIdentifyProvider(UserIdentifyProvider):
    def __init__(self, context: TelegramContextDTO):
        self._ctx: TelegramContextDTO = context

    async def get_user_id(self) -> UserId:
        return UserId(self._ctx.user_id)

    async def get_role(self) -> UserRole:
        return self._ctx.user_role
