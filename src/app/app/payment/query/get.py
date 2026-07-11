from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.payment.dto.payment import PaymentDTO
from app.app.payment.port import PaymentReader
from app.domain.payment.exception import PaymentNotFoundError
from app.domain.payment.service import PaymentAccessService
from app.domain.payment.value_object import PaymentId
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetPaymentQuery:
    id: UUID


class GetPayment:
    def __init__(self, actor_provider: ActorProvider, reader: PaymentReader):
        self._actor_provider = actor_provider
        self._reader = reader

    async def __call__(self, query: GetPaymentQuery) -> PaymentDTO:
        payment: PaymentDTO | None = await self._reader.read(
            payment_id=PaymentId(query.id),
        )
        if not payment:
            raise PaymentNotFoundError

        PaymentAccessService.ensure_can_view(
            actor=await self._actor_provider.get(),
            payment_creator_id=UserId(payment.creator_id),
        )

        return payment
