from dishka import Provider, Scope, provide, provide_all

from app.app.wallet.cmd import (
    CancelTopUp,
    ConfirmTopUp,
    CreateTopUpPayment,
    TopUpWalletManually,
)
from app.app.wallet.port import WalletReader
from app.app.wallet.query import (
    GetWalletsByUserId,
    ListWalletsByUserId,
)
from app.domain.wallet.port import WalletRepository
from app.infra.wallet import SqlAWalletReader, SqlAWalletRepository


class WalletHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        ConfirmTopUp, CreateTopUpPayment, TopUpWalletManually, CancelTopUp
    )

    queries = provide_all(GetWalletsByUserId, GetWalletsByUserId, ListWalletsByUserId)


class WalletAdaptersProvider(Provider):
    scope = Scope.REQUEST

    reader = provide(SqlAWalletReader, provides=WalletReader)

    repository = provide(SqlAWalletRepository, provides=WalletRepository)
