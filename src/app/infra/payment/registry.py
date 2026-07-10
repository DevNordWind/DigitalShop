from typing import override

from dishka import AsyncContainer
from frozendict import frozendict

from app.app.order.cmd import ConfirmOrder
from app.app.payment.port import PaymentPurposeHandler, PaymentPurposeHandlersRegistry
from app.app.wallet.cmd import ConfirmTopUp
from app.domain.payment.enums import PaymentPurposeType

_MAPPING: dict[PaymentPurposeType, type[PaymentPurposeHandler]] = {
    PaymentPurposeType.WALLET_TOP_UP: ConfirmTopUp,
    PaymentPurposeType.ORDER_PAYMENT: ConfirmOrder,
}


class DishkaPaymentPurposeHandlersRegistry(PaymentPurposeHandlersRegistry):
    MAPPING: frozendict[PaymentPurposeType, type[PaymentPurposeHandler]] = frozendict(
        _MAPPING
    )

    def __init__(self, container: AsyncContainer):
        self._container: AsyncContainer = container

    @override
    async def get(
        self,
        purpose_type: PaymentPurposeType,
    ) -> PaymentPurposeHandler:
        return await self._container.get(self.MAPPING[purpose_type])
