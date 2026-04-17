from dishka import AsyncContainer

from app.order.cmd import ConfirmOrder
from app.payment.port import (
    PaymentPurposeHandler,
    PaymentPurposeHandlersRegistry,
)
from app.wallet.cmd.confirm_top_up import ConfirmTopUp
from domain.payment.enums import PaymentPurposeType


class PaymentPurposeHandlersRegistryImpl(PaymentPurposeHandlersRegistry):
    def __init__(self, container: AsyncContainer):
        self._container: AsyncContainer = container

    async def get(
        self,
        purpose_type: PaymentPurposeType,
    ) -> PaymentPurposeHandler | None:
        match purpose_type:
            case PaymentPurposeType.WALLET_TOP_UP:
                return await self._container.get(ConfirmTopUp)
            case PaymentPurposeType.ORDER_PAYMENT:
                return await self._container.get(ConfirmOrder)
