from typing import override

from dishka import AsyncContainer

from app.app.order.cmd import ConfirmOrder
from app.app.payment.port import PaymentPurposeHandler, PaymentPurposeHandlersRegistry
from app.app.wallet.cmd import ConfirmTopUp
from app.domain.payment.enums import PaymentPurposeType


class DishkaPaymentPurposeHandlersRegistry(PaymentPurposeHandlersRegistry):
    def __init__(self, container: AsyncContainer):
        self._container: AsyncContainer = container

    @override
    async def get(
        self,
        purpose_type: PaymentPurposeType,
    ) -> PaymentPurposeHandler | None:
        match purpose_type:
            case PaymentPurposeType.WALLET_TOP_UP:
                return await self._container.get(ConfirmTopUp)
            case PaymentPurposeType.ORDER_PAYMENT:
                return await self._container.get(ConfirmOrder)
