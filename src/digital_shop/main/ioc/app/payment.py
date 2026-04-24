from app.payment.cmd import (
    CancelPayment,
    ChangePaymentCommissionCoefficient,
    CheckPayment,
    ConfirmPayment,
)
from app.payment.query import GetPayment, GetPaymentCommission
from dishka import Provider, Scope, provide_all


class PaymentHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        ConfirmPayment,
        CheckPayment,
        CancelPayment,
        ChangePaymentCommissionCoefficient,
    )

    queries = provide_all(GetPayment, GetPaymentCommission)
