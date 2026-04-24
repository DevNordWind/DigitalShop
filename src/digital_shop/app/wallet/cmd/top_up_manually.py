import asyncio
from asyncio import Task
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.common.dto.money import MoneyDTO, MoneyMapper
from app.common.port import DatabaseSession, TelegramNotification
from app.common.port.telegram_notification import NotificationRequest
from app.user.exception import UserNotFound
from app.user.service import GetCurrentUser
from domain.user.entity import User
from domain.user.value_object import UserId
from domain.wallet.entity import Wallet
from domain.wallet.exception import WalletPermissionDenied
from domain.wallet.port import WalletRepository
from domain.wallet.service import WalletAccessService


@dataclass(slots=True, frozen=True)
class TopUpWalletManuallyCmd:
    amount: MoneyDTO
    target_user_id: UUID


class TopUpWalletManually:
    def __init__(
        self,
        wallet_repo: WalletRepository,
        current_user: GetCurrentUser,
        notification: TelegramNotification,
        session: DatabaseSession,
    ):
        self._wallet_repo: WalletRepository = wallet_repo
        self._current_user: GetCurrentUser = current_user
        self._notification: TelegramNotification = notification
        self._session: DatabaseSession = session
        self._tasks: set[Task[Any]] = set()

    async def __call__(self, cmd: TopUpWalletManuallyCmd) -> None:
        amount = MoneyMapper.to_value_object(src=cmd.amount)
        target_user_id: UserId = UserId(cmd.target_user_id)

        actor: User = await self._current_user()
        if not WalletAccessService.can_top_up_manually(actor_role=actor.role):
            raise WalletPermissionDenied

        wallet: (
            Wallet | None
        ) = await self._wallet_repo.get_by_currency_for_update(
            user_id=target_user_id, currency=cmd.amount.currency
        )
        if not wallet:
            raise UserNotFound

        wallet.top_up(amount=amount)
        await self._session.commit()

        self._tasks.add(
            asyncio.create_task(
                self._notification.send(
                    user_id=target_user_id,
                    request=NotificationRequest(
                        key="admin-top-up-notification"
                    ),
                    amount=amount.amount,
                    currency=amount.currency,
                )
            )
        )
