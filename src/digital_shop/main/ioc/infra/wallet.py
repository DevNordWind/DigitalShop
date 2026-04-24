from app.wallet.port import WalletReader
from dishka import Provider, Scope, provide
from domain.wallet.port import WalletRepository
from infra.wallet.reader import WalletReaderImpl
from infra.wallet.repository import WalletRepositoryImpl


class WalletAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(WalletRepositoryImpl, provides=WalletRepository)

    reader = provide(WalletReaderImpl, provides=WalletReader)
