from app.app.common.dto.coefficient import CoefficientMapper
from app.app.common.exception import DataCorruptionError
from app.app.common.port.session import DatabaseSession
from app.app.common.port.telegram_notification import (
    NotificationRequest,
    TelegramNotification,
)
from app.app.order.dto.order import OrderDTO
from app.domain.common.port import Clock
from app.domain.order.entity import Order
from app.domain.order.port import OrderRepository
from app.domain.referral.entity import ReferralAward, ReferrerProfile
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

    async def apply(self, order: Order) -> None:
        profile: ReferrerProfile | None = await self._arrange_profile(
            customer_id=order.customer_id
        )
        if profile is None:
            return

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

    async def notify(self, order: OrderDTO) -> None:
        profile: ReferrerProfile | None = await self._arrange_profile(
            customer_id=UserId(order.customer_id)
        )
        if profile is None:
            return

        award: ReferralAward | None = await self._award_repo.get_by_reference_id(
            reference_id=order.id
        )
        if award is None:
            raise DataCorruptionError("Award not created")

        if profile.send_notifications and award.status == ReferralAwardStatus.COMPLETED:
            (
                await self._notification.send(
                    user_id=profile.user_id,
                    request=NotificationRequest(
                        key="referral-award-notification",
                    ),
                    amount=award.award.amount if award.award else None,
                    currency=award.award.currency if award.award else None,
                    percent=CoefficientMapper.to_dto(
                        src=award.coefficient_snapshot
                    ).as_percent,
                ),
            )

    async def _arrange_profile(self, customer_id: UserId) -> ReferrerProfile | None:
        customer: User | None = await self._user_repo.get(customer_id)
        if customer is None:
            raise DataCorruptionError("Order exists without user")

        if customer.referrer_id is None:
            return None

        profile: ReferrerProfile | None = await self._profile_repo.get(
            user_id=customer.referrer_id,
        )
        if profile is None:
            raise DataCorruptionError("Referrer_id exists without user")

        return profile
