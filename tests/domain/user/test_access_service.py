from typing import Final
from uuid import UUID

import pytest

from app.domain.common.actor import UserActor
from app.domain.user.enums import UserRole
from app.domain.user.exception import UserPermissionDeniedError
from app.domain.user.service import UserAccessService
from app.domain.user.value_object import UserId

FIXED_UUID: Final[UUID] = UUID("019f20ff-62b9-720b-8e19-3171139ddd0d")


def make_user_actor(role: UserRole) -> UserActor:
    return UserActor(id=UserId(value=FIXED_UUID), role=role)


class TestUserAccessService:
    @pytest.mark.parametrize(
        "actor_role, target_current_role, target_role",  # noqa: PT006
        [
            pytest.param(
                UserRole.SUPER_ADMIN,
                UserRole.USER,
                UserRole.ADMIN,
                id="super_admin_can_promote_user_to_admin",
            ),
            pytest.param(
                UserRole.SUPER_ADMIN,
                UserRole.ADMIN,
                UserRole.USER,
                id="super_admin_can_demote_admin_to_user",
            ),
            pytest.param(
                UserRole.SUPER_ADMIN,
                UserRole.USER,
                UserRole.USER,
                id="super_admin_can_reassign_user_to_same_role",
            ),
        ],
    )
    def test_can_assign_role_permitted(
        self,
        actor_role: UserRole,
        target_current_role: UserRole,
        target_role: UserRole,
    ) -> None:
        UserAccessService.ensure_can_assign_role(
            actor=make_user_actor(role=actor_role),
            target_current_role=target_current_role,
            target_role=target_role,
        )

    @pytest.mark.parametrize(
        "actor_role, target_current_role, target_role",  # noqa: PT006
        [
            pytest.param(
                UserRole.ADMIN,
                UserRole.USER,
                UserRole.ADMIN,
                id="admin_cannot_promote_to_own_level",
            ),
            pytest.param(
                UserRole.ADMIN,
                UserRole.USER,
                UserRole.SUPER_ADMIN,
                id="admin_cannot_promote_above_own_level",
            ),
            pytest.param(
                UserRole.ADMIN,
                UserRole.ADMIN,
                UserRole.USER,
                id="admin_cannot_demote_peer_admin",
            ),
            pytest.param(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.USER,
                id="admin_cannot_demote_super_admin",
            ),
            pytest.param(
                UserRole.USER,
                UserRole.USER,
                UserRole.USER,
                id="user_cannot_assign_peer",
            ),
            pytest.param(
                UserRole.USER,
                UserRole.USER,
                UserRole.ADMIN,
                id="user_cannot_promote_to_admin",
            ),
            pytest.param(
                UserRole.USER,
                UserRole.USER,
                UserRole.SUPER_ADMIN,
                id="user_cannot_promote_to_super_admin",
            ),
            pytest.param(
                UserRole.SUPER_ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.SUPER_ADMIN,
                id="super_admin_cannot_act_on_super_admin",
            ),
            pytest.param(
                UserRole.SUPER_ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.USER,
                id="super_admin_cannot_demote_peer_super_admin",
            ),
        ],
    )
    def test_can_assign_role_denied(
        self,
        actor_role: UserRole,
        target_current_role: UserRole,
        target_role: UserRole,
    ) -> None:
        with pytest.raises(UserPermissionDeniedError):
            UserAccessService.ensure_can_assign_role(
                actor=make_user_actor(role=actor_role),
                target_current_role=target_current_role,
                target_role=target_role,
            )
