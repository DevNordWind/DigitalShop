import pytest

from app.domain.user.enums.role import UserRole
from app.domain.user.value_object import UserId
from app.domain.wallet.exception import WalletPermissionDeniedError
from app.domain.wallet.service import WalletAccessService
from tests.const import FIXED_UUID
from tests.factory import SystemActorFactory, UserActorFactory


class TestWalletAccessServiceEnsureCanTopPayment:
    def test_raises_permission_denied_on_system_actor(self) -> None:
        # Arrange
        actor = SystemActorFactory.build()

        # Act & Assert
        with pytest.raises(WalletPermissionDeniedError):
            WalletAccessService.ensure_can_top_up_payment(actor=actor)

    def test_returns_actor_on_user_actor(self) -> None:
        # Arrange
        actor = UserActorFactory.build()

        # Act
        result = WalletAccessService.ensure_can_top_up_payment(actor=actor)

        # Assert
        assert actor == result


class TestWalletAccessServiceEnsureCanCancelTopUpPayment:
    def test_got_permission_on_system_actor(self) -> None:
        # Arrange
        actor = SystemActorFactory.build()

        # Act
        WalletAccessService.ensure_can_cancel_top_up_payment(
            actor=actor, payment_creator_id=UserId(FIXED_UUID)
        )

    def test_got_permission_on_user_actor_admin(
        self,
    ) -> None:
        # Arrange
        actor = UserActorFactory.build(role=UserRole.ADMIN)

        # Act
        WalletAccessService.ensure_can_cancel_top_up_payment(
            actor=actor, payment_creator_id=UserId(FIXED_UUID)
        )

    def test_got_permission_if_actor_is_payment_creator(
        self,
    ) -> None:
        # Arrange
        user_id = UserId(FIXED_UUID)
        actor = UserActorFactory.build(id=user_id)

        # Act
        WalletAccessService.ensure_can_cancel_top_up_payment(
            actor=actor, payment_creator_id=user_id
        )

    def test_raises_permission_denied_if_actor_is_not_payment_creator(
        self,
    ) -> None:
        # Arrange
        actor = UserActorFactory.build()

        # Act & Assert
        with pytest.raises(WalletPermissionDeniedError):
            WalletAccessService.ensure_can_cancel_top_up_payment(
                actor=actor, payment_creator_id=UserId(FIXED_UUID)
            )


class TestWalletAccessServiceEnsureCanTopUpManually:
    def test_got_permission_on_system_actor(self) -> None:
        # Arrange
        actor = SystemActorFactory.build()

        # Act
        WalletAccessService.ensure_can_top_up_manually(actor=actor)

    def test_got_permission_on_user_actor_admin(
        self,
    ) -> None:
        # Arrange
        actor = UserActorFactory.build(role=UserRole.ADMIN)

        # Act
        WalletAccessService.ensure_can_top_up_manually(
            actor=actor,
        )

    def test_raises_permission_denied_if_user_actor_is_not_admin(
        self,
    ) -> None:
        # Arrange
        actor = UserActorFactory.build()

        # Act & Assert
        with pytest.raises(WalletPermissionDeniedError):
            WalletAccessService.ensure_can_top_up_manually(
                actor=actor,
            )


class TestWalletAccessServiceEnsureCanView:
    def test_got_permission_on_system_actor(self) -> None:
        # Arrange
        actor = SystemActorFactory.build()

        # Act
        WalletAccessService.ensure_can_view(
            actor=actor, target_user_id=UserId(FIXED_UUID)
        )

    def test_got_permission_on_user_actor_admin(
        self,
    ) -> None:
        # Arrange
        actor = UserActorFactory.build(role=UserRole.ADMIN)

        # Act
        WalletAccessService.ensure_can_view(
            actor=actor, target_user_id=UserId(FIXED_UUID)
        )

    def test_got_permission_if_user_actor_is_wallet_owner(
        self,
    ) -> None:
        # Arrange
        user_id = UserId(FIXED_UUID)
        actor = UserActorFactory.build(id=user_id)

        # Act
        WalletAccessService.ensure_can_view(actor=actor, target_user_id=user_id)

    def test_raises_permission_denied_if_user_actor_is_not_wallet_owner(
        self,
    ) -> None:
        # Arrange
        actor = UserActorFactory.build()

        # Act & Assert
        with pytest.raises(WalletPermissionDeniedError):
            WalletAccessService.ensure_can_view(
                actor=actor, target_user_id=UserId(FIXED_UUID)
            )
