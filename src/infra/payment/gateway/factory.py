from dishka import AsyncContainer
from frozendict import frozendict

from app.payment.port import (
    PaymentMethodGateway,
    PaymentMethodGatewayFactory,
    UnsupportedPaymentMethod,
)
from domain.payment.enums import PaymentMethod
from infra.payment.gateway.crypto_pay import CryptoPayPaymentGateway


class PaymentMethodGatewayFactoryImpl(PaymentMethodGatewayFactory):
    MAPPING: frozendict[PaymentMethod, type[PaymentMethodGateway]] = (
        frozendict({PaymentMethod.CRYPTO_PAY: CryptoPayPaymentGateway})
    )

    def __init__(self, container: AsyncContainer):
        self._container: AsyncContainer = container

    async def get(self, method: PaymentMethod) -> PaymentMethodGateway:
        try:
            gateway_tp: type[PaymentMethodGateway] = self.MAPPING[method]
        except KeyError as e:
            raise UnsupportedPaymentMethod from e

        return await self._container.get(gateway_tp)
