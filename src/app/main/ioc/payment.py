from dishka import Provider, Scope, provide, provide_all

from app.app.payment.cmd import (
    ChangePaymentCommissionCoefficient,
    CheckPayment,
    ConfirmPayment,
)
from app.app.payment.port import (
    PaymentMethodGatewayFactory,
    PaymentPurposeHandlersRegistry,
    PaymentReader,
)
from app.app.payment.query import GetPayment, GetPaymentCommission
from app.app.payment.service import PaymentApplicationService
from app.domain.payment.port import PaymentCommissionRuleRepository, PaymentRepository
from app.domain.payment.service import PaymentDomainService
from app.infra.payment import (
    CryptoPayPaymentGateway,
    DishkaPaymentMethodGatewayFactory,
    DishkaPaymentPurposeHandlersRegistry,
    SqlAPaymentCommissionRuleRepository,
    SqlAPaymentReader,
    SqlAPaymentRepository,
)


class PaymentDomainServicesProvider(Provider):
    scope = Scope.APP

    service = provide(PaymentDomainService)


class PaymentHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        ChangePaymentCommissionCoefficient,
        CheckPayment,
        ConfirmPayment,
    )

    queries = provide_all(GetPayment, GetPaymentCommission)

    services = provide_all(PaymentApplicationService)


class PaymentAdaptersProvider(Provider):
    scope = Scope.REQUEST

    reader = provide(SqlAPaymentReader, provides=PaymentReader)

    repository = provide(SqlAPaymentRepository, provides=PaymentRepository)
    commission_repository = provide(
        SqlAPaymentCommissionRuleRepository, provides=PaymentCommissionRuleRepository
    )

    crypto_pay_gateway = provide(CryptoPayPaymentGateway, scope=Scope.APP)

    gateway_factory = provide(
        DishkaPaymentMethodGatewayFactory,
        provides=PaymentMethodGatewayFactory,
        scope=Scope.APP,
    )

    registry = provide(
        DishkaPaymentPurposeHandlersRegistry, provides=PaymentPurposeHandlersRegistry
    )
