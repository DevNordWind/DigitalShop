from typing import override

from app.app.common.port.actor_provider import ActorProvider
from app.domain.common.actor import UserActor
from app.domain.user.value_object import UserId
from app.infra.authentication.telegram.dto import TelegramContextDTO


class AiogramActorProvider(ActorProvider):
    def __init__(self, context: TelegramContextDTO):
        self._ctx: TelegramContextDTO = context

    @override
    async def get(self) -> UserActor:
        return UserActor(id=UserId(value=self._ctx.user_id), role=self._ctx.user_role)
