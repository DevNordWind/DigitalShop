from app.payment.port import (
    PaymentMethodGatewayFactory,
    PaymentPurposeHandlersRegistry,
    PaymentReader,
)
from dishka import Provider, Scope, provide
from domain.payment.port import (
    PaymentCommissionRuleRepository,
    PaymentRepository,
)
from infra.payment.gateway import (
    CryptoPayPaymentGateway,
    PaymentMethodGatewayFactoryImpl,
)
from infra.payment.reader import PaymentReaderImpl
from infra.payment.registry import PaymentPurposeHandlersRegistryImpl
from infra.payment.repository import PaymentRepositoryImpl
from infra.payment.rule_repository import PaymentCommissionRuleRepositoryImpl


class PaymentAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(
        PaymentRepositoryImpl,
        provides=PaymentRepository,
    )

    reader = provide(PaymentReaderImpl, provides=PaymentReader)

    registry = provide(
        PaymentPurposeHandlersRegistryImpl,
        provides=PaymentPurposeHandlersRegistry,
    )

    payment_factory = provide(
        PaymentMethodGatewayFactoryImpl,
        provides=PaymentMethodGatewayFactory,
        scope=Scope.APP,
    )

    crypto_bot_gateway = provide(CryptoPayPaymentGateway, scope=Scope.APP)

    rule_repository = provide(
        PaymentCommissionRuleRepositoryImpl,
        provides=PaymentCommissionRuleRepository,
    )
