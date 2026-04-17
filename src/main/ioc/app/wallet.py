from dishka import Provider, Scope, provide, provide_all

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


class WalletHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        CreateTopUpPayment, ConfirmTopUp, TopUpWalletManually
    )

    queries = provide_all(
        provide(GetMyWallets),
        provide(GetMyWalletsWithTotal),
        provide(ListWalletsByUserId),
    )
