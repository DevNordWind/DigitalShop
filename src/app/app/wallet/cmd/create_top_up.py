from dataclasses import dataclass

from app.app.common.dto.money import MoneyDTO, MoneyMapper
from app.app.common.exception import DataCorruptionError
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.payment.port.payment import Invoice
from app.app.payment.service import (
    CreatedPayment,
    CreatePaymentData,
    FailedCreatedPayment,
    PaymentApplicationService,
)
from app.domain.common.actor import UserActor
from app.domain.common.money import Money
from app.domain.common.port import Clock
from app.domain.payment.enums import PaymentMethod, PaymentPurposeType
from app.domain.payment.value_object import PaymentPurpose
from app.domain.wallet.entity import Wallet
from app.domain.wallet.port import WalletRepository
from app.domain.wallet.service import WalletAccessService


@dataclass(slots=True, frozen=True)
class CreateTopUpPaymentCmd:
    amount: MoneyDTO
    method: PaymentMethod


class CreateTopUpPayment:
    def __init__(
        self,
        repo: WalletRepository,
        payment_service: PaymentApplicationService,
        actor_provider: ActorProvider,
        clock: Clock,
        session: DatabaseSession,
    ):
        self._repo = repo
        self._payment_service = payment_service
        self._actor_provider = actor_provider
        self._clock = clock
        self._session = session

    async def __call__(self, cmd: CreateTopUpPaymentCmd) -> Invoice:
        actor: UserActor = WalletAccessService.ensure_can_top_up_payment(
            actor=await self._actor_provider.get()
        )

        amount: Money = MoneyMapper.to_value_object(src=cmd.amount)
        wallet: Wallet | None = await self._repo.get_by_user_id_currency(
            user_id=actor.id, currency=amount.currency
        )
        if not wallet:
            raise DataCorruptionError(
                f"User {actor.id} exists but its wallet was not found",
            )

        wallet.ensure_can_top_up(amount=amount)

        created_payment: CreatedPayment = await self._payment_service.create(
            data=CreatePaymentData(
                actor=actor,
                purpose=PaymentPurpose(
                    reference_id=wallet.id.value, type=PaymentPurposeType.WALLET_TOP_UP
                ),
                method=cmd.method,
                amount=amount,
            )
        )

        if isinstance(created_payment, FailedCreatedPayment):
            await self._session.commit()
            raise created_payment.e

        await self._session.commit()
        return created_payment.invoice
