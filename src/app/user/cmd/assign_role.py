from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.user.exception import UserNotFound
from app.user.port import UserIdentifyProvider
from domain.user.enums import UserRole
from domain.user.exception import UserPermissionDenied
from domain.user.port import UserRepository
from domain.user.service import UserAccessService
from domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class AssignUserRoleCmd:
    target_user_id: UUID
    target_role: UserRole


class AssignUserRole:
    def __init__(
        self,
        repository: UserRepository,
        session: DatabaseSession,
        idp: UserIdentifyProvider,
    ):
        self._repository: UserRepository = repository
        self._session: DatabaseSession = session
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, cmd: AssignUserRoleCmd) -> None:
        assigner_role = await self._idp.get_role()

        target_user = await self._repository.get(
            user_id=UserId(cmd.target_user_id)
        )
        if not target_user:
            raise UserNotFound

        if not UserAccessService.can_assign_role(
            assigner_role=assigner_role,
            target_current_role=target_user.role,
            target_role=cmd.target_role,
        ):
            raise UserPermissionDenied

        target_user.assign_role(role=cmd.target_role)
        await self._session.commit()
