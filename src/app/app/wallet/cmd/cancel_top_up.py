from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.payment.service import PaymentApplicationService
from app.app.payment.service.service import CancelPaymentData
from app.domain.common.port import Clock
from app.domain.payment.entity import Payment
from app.domain.wallet.port import WalletRepository
from app.domain.wallet.service import WalletAccessService


@dataclass(slots=True, frozen=True)
class CancelTopUpCmd:
    payment_id: UUID


class CancelTopUp:
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

    async def __call__(self, cmd: CancelTopUpCmd) -> None:
        payment: Payment = await self._payment_service.cancel(
            data=CancelPaymentData(id=cmd.payment_id)
        )
        WalletAccessService.ensure_can_cancel_top_up_payment(
            actor=await self._actor_provider.get(), user_id=payment.creator_id
        )
        await self._session.commit()
