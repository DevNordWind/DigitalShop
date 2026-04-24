from app.wallet.cmd import (
    ConfirmTopUp,
    CreateTopUpPayment,
    TopUpWalletManually,
)
from app.wallet.query import (
    GetMyWallets,
    GetMyWalletsWithTotal,
    ListWalletsByUserId,
)
from dishka import Provider, Scope, provide_all


class WalletHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        CreateTopUpPayment, ConfirmTopUp, TopUpWalletManually
    )

    queries = provide_all(
        GetMyWallets,
        GetMyWalletsWithTotal,
        ListWalletsByUserId,
    )
