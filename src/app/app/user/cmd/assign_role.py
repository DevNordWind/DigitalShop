from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.user.enums import UserRole
from app.domain.user.exception import UserNotFoundError
from app.domain.user.port import UserRepository
from app.domain.user.service import UserAccessService
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class AssignUserRoleCmd:
    target_user_id: UUID
    target_role: UserRole


class AssignUserRole:
    def __init__(
        self,
        repo: UserRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
    ):
        self._repo = repo
        self._session = session
        self._actor_provider = actor_provider

    async def __call__(self, cmd: AssignUserRoleCmd) -> None:
        target_user = await self._repo.get(user_id=UserId(cmd.target_user_id))
        if not target_user:
            raise UserNotFoundError

        UserAccessService.ensure_can_assign_role(
            actor=await self._actor_provider.get(),
            target_current_role=target_user.role,
            target_role=cmd.target_role,
        )

        target_user.assign_role(role=cmd.target_role)
        await self._session.commit()
