from typing import override

from dishka import AsyncContainer
from frozendict import frozendict

from app.app.payment.port import (
    PaymentMethodGateway,
    PaymentMethodGatewayFactory,
    UnsupportedPaymentMethodError,
)
from app.domain.payment.enums import PaymentMethod
from app.infra.payment.gateway import CryptoPayPaymentGateway


class DishkaPaymentMethodGatewayFactory(PaymentMethodGatewayFactory):
    MAPPING: frozendict[PaymentMethod, type[PaymentMethodGateway]] = frozendict(
        {PaymentMethod.CRYPTO_PAY: CryptoPayPaymentGateway}
    )

    def __init__(self, container: AsyncContainer):
        self._container: AsyncContainer = container

    @override
    async def get(self, method: PaymentMethod) -> PaymentMethodGateway:
        try:
            gateway_tp: type[PaymentMethodGateway] = self.MAPPING[method]
        except KeyError as e:
            raise UnsupportedPaymentMethodError from e

        return await self._container.get(gateway_tp)
