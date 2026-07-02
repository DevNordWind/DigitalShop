import asyncio
from asyncio import Task
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.app.common.dto.money import MoneyDTO, MoneyMapper
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.common.port.telegram_notification import (
    NotificationRequest,
    TelegramNotification,
)
from app.domain.user.exception import UserNotFoundError
from app.domain.user.value_object import UserId
from app.domain.wallet.entity import Wallet
from app.domain.wallet.port import WalletRepository
from app.domain.wallet.service import WalletAccessService


@dataclass(slots=True, frozen=True)
class TopUpWalletManuallyCmd:
    amount: MoneyDTO
    target_user_id: UUID


class TopUpWalletManually:
    def __init__(
        self,
        wallet_repo: WalletRepository,
        actor_provider: ActorProvider,
        notification: TelegramNotification,
        session: DatabaseSession,
    ):
        self._wallet_repo = wallet_repo
        self._actor_provider = actor_provider
        self._notification = notification
        self._session = session
        self._tasks: set[Task[Any]] = set()

    async def __call__(self, cmd: TopUpWalletManuallyCmd) -> None:
        amount = MoneyMapper.to_value_object(src=cmd.amount)
        target_user_id: UserId = UserId(cmd.target_user_id)

        WalletAccessService.ensure_can_top_up_manually(
            actor=await self._actor_provider.get()
        )

        wallet: Wallet | None = await self._wallet_repo.acquire_user_id_by_currency(
            user_id=target_user_id, currency=cmd.amount.currency
        )
        if not wallet:
            raise UserNotFoundError

        wallet.top_up(amount=amount)
        await self._session.commit()

        self._tasks.add(
            asyncio.create_task(
                self._notification.send(
                    user_id=target_user_id,
                    request=NotificationRequest(key="admin-top-up-notification"),
                    amount=amount.amount,
                    currency=amount.currency,
                )
            )
        )
