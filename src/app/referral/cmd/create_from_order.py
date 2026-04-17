import asyncio
from asyncio import Task
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.common.exception import DataCorruptionError
from app.common.port import DatabaseSession, TelegramNotification
from app.common.port.telegram_notification import NotificationRequest
from app.order.exception import OrderNotFound
from app.referral.dto.award import ReferralAwardMapper
from app.referral.dto.profile import ReferrerProfileMapper
from domain.common.port import Clock
from domain.order.entity import Order
from domain.order.port.repository import OrderRepository
from domain.order.value_object import OrderId
from domain.referral.entity import ReferrerProfile
from domain.referral.enums import ReferralAwardSourceType
from domain.referral.enums.status import ReferralAwardStatus
from domain.referral.policy import ReferralPolicy
from domain.referral.port import (
    ReferralAwardRepository,
    ReferralPolicyRepository,
    ReferrerProfileRepository,
)
from domain.referral.service.award_service import ReferralAwardService
from domain.referral.value_object import ReferralAwardSource
from domain.user.entity import User
from domain.user.port import UserRepository
from domain.user.value_object import UserId
from domain.wallet.entity import Wallet
from domain.wallet.port import WalletRepository


@dataclass(slots=True, frozen=True)
class CreateReferralAwardFromOrderCmd:
    order_id: UUID


class CreateReferralAwardFromOrder:
    def __init__(
        self,
        order_repo: OrderRepository,
        user_repo: UserRepository,
        profile_repo: ReferrerProfileRepository,
        award_repo: ReferralAwardRepository,
        policy_repo: ReferralPolicyRepository,
        referral_service: ReferralAwardService,
        wallet_repo: WalletRepository,
        session: DatabaseSession,
        notification: TelegramNotification,
        clock: Clock,
    ):
        self._order_repo: OrderRepository = order_repo
        self._user_repo: UserRepository = user_repo
        self._profile_repo: ReferrerProfileRepository = profile_repo
        self._award_repo: ReferralAwardRepository = award_repo
        self._ref_service: ReferralAwardService = referral_service
        self._policy_repo: ReferralPolicyRepository = policy_repo
        self._wallet_repo: WalletRepository = wallet_repo
        self._notification: TelegramNotification = notification
        self._session: DatabaseSession = session
        self._clock: Clock = clock
        self._tasks: set[Task[Any]] = set()

    async def __call__(self, cmd: CreateReferralAwardFromOrderCmd) -> None:
        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.order_id),
        )
        if not order:
            raise OrderNotFound

        customer: User | None = await self._user_repo.get(order.customer_id)
        if customer is None:
            raise DataCorruptionError

        if customer.referrer_id is None:
            return

        profile: ReferrerProfile | None = await self._profile_repo.get(
            user_id=customer.referrer_id,
        )
        if profile is None:
            raise DataCorruptionError

        policy: ReferralPolicy = await self._policy_repo.get()

        award = await self._ref_service.create(
            profile=profile,
            policy=policy,
            total=order.total,
            source=ReferralAwardSource(
                reference_id=order.id.value,
                type=ReferralAwardSourceType.ORDER,
                amount=order.total,
            ),
        )
        await self._award_repo.add(award)
        await self._session.flush()
        if (
            award.status == ReferralAwardStatus.COMPLETED
            and award.award is not None
        ):
            wallet: (
                Wallet | None
            ) = await self._wallet_repo.get_by_currency_for_update(
                user_id=profile.user_id,
                currency=profile.award_currency,
            )
            if wallet is None:
                raise DataCorruptionError
            wallet.top_up(amount=award.award)

        profile_dto = ReferrerProfileMapper.to_dto(src=profile)
        award_dto = ReferralAwardMapper.to_dto(src=award)

        await self._session.commit()

        if (
            profile_dto.send_notifications
            and award_dto.status == ReferralAwardStatus.COMPLETED
        ):
            task = asyncio.create_task(
                self._notification.send(
                    user_id=UserId(profile_dto.user_id),
                    request=NotificationRequest(
                        key="referral-award-notification",
                    ),
                    amount=award_dto.award.amount if award_dto.award else None,
                    currency=award_dto.award.currency
                    if award_dto.award
                    else None,
                    percent=award_dto.coefficient_snapshot.as_percent,
                ),
            )
            self._tasks.add(task)
