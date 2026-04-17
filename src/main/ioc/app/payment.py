from dishka import Provider, Scope, provide, provide_all

from app.payment.cmd import (
    CancelPayment,
    ChangePaymentCommissionCoefficient,
    CheckPayment,
    ConfirmPayment,
)
from app.payment.query import GetPayment, GetPaymentCommission


class PaymentHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        provide(ConfirmPayment),
        provide(CheckPayment),
        provide(CancelPayment),
        provide(ChangePaymentCommissionCoefficient),
    )

    queries = provide_all(provide(GetPayment), provide(GetPaymentCommission))
