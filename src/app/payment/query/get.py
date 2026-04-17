from dataclasses import dataclass
from uuid import UUID

from app.payment.dto.payment import PaymentDTO
from app.payment.exception import PaymentNotFound
from app.payment.port import PaymentReader
from app.user.service import GetCurrentUser
from domain.payment.exception import PaymentPermissionDenied
from domain.payment.service import PaymentAccessService
from domain.payment.value_object import PaymentId
from domain.user.entity import User
from domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetPaymentQuery:
    id: UUID


class GetPayment:
    def __init__(self, current_user: GetCurrentUser, reader: PaymentReader):
        self._current_user: GetCurrentUser = current_user
        self._reader: PaymentReader = reader

    async def __call__(self, query: GetPaymentQuery) -> PaymentDTO:
        dto: PaymentDTO | None = await self._reader.read(
            payment_id=PaymentId(query.id),
        )
        if not dto:
            raise PaymentNotFound

        viewer: User = await self._current_user()

        if not PaymentAccessService.can_view(
            viewer=viewer, payment_creator_id=UserId(dto.creator_id)
        ):
            raise PaymentPermissionDenied

        return dto
