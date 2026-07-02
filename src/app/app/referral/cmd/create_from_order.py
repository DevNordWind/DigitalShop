import asyncio
from asyncio import Task
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.app.common.exception import DataCorruptionError
from app.app.common.port.session import DatabaseSession
from app.app.common.port.telegram_notification import (
    NotificationRequest,
    TelegramNotification,
)
from app.app.referral.dto.award import ReferralAwardMapper
from app.app.referral.dto.profile import ReferrerProfileMapper
from app.domain.common.port import Clock
from app.domain.order.entity import Order
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.port import OrderRepository
from app.domain.order.value_object import OrderId
from app.domain.referral.entity import ReferrerProfile
from app.domain.referral.enums import ReferralAwardSourceType, ReferralAwardStatus
from app.domain.referral.policy import ReferralPolicy
from app.domain.referral.port import (
    ReferralAwardRepository,
    ReferralPolicyRepository,
    ReferrerProfileRepository,
)
from app.domain.referral.service import ReferralAwardDomainService
from app.domain.referral.value_object import ReferralAwardSource
from app.domain.user.entity import User
from app.domain.user.port import UserRepository
from app.domain.user.value_object import UserId
from app.domain.wallet.entity import Wallet
from app.domain.wallet.port import WalletRepository


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
        referral_service: ReferralAwardDomainService,
        wallet_repo: WalletRepository,
        session: DatabaseSession,
        notification: TelegramNotification,
        clock: Clock,
    ):
        self._order_repo = order_repo
        self._user_repo = user_repo
        self._profile_repo = profile_repo
        self._award_repo = award_repo
        self._ref_service = referral_service
        self._policy_repo = policy_repo
        self._wallet_repo = wallet_repo
        self._notification = notification
        self._session = session
        self._clock = clock
        self._tasks: set[Task[Any]] = set()

    async def __call__(self, cmd: CreateReferralAwardFromOrderCmd) -> None:
        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.order_id),
        )
        if not order:
            raise OrderNotFoundError

        customer: User | None = await self._user_repo.get(order.customer_id)
        if customer is None:
            raise DataCorruptionError("Order exists without user")

        if customer.referrer_id is None:
            return

        profile: ReferrerProfile | None = await self._profile_repo.get(
            user_id=customer.referrer_id,
        )
        if profile is None:
            raise DataCorruptionError("Referrer_id exists without user")

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
        await self._award_repo.add(award=award)
        await self._session.flush()
        if award.status == ReferralAwardStatus.COMPLETED and award.award is not None:
            wallet: Wallet | None = await self._wallet_repo.acquire_user_id_by_currency(
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
                    currency=award_dto.award.currency if award_dto.award else None,
                    percent=award_dto.coefficient_snapshot.as_percent,
                ),
            )
            self._tasks.add(task)
