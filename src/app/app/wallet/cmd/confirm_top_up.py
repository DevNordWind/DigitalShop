from typing import override

from app.app.common.dto.money import MoneyMapper
from app.app.common.exception import DataCorruptionError
from app.app.common.port.session import DatabaseSession
from app.app.common.port.telegram_notification import (
    TelegramNotification,
)
from app.app.payment.dto.payment import PaymentDTO
from app.app.payment.port import (
    PaymentPurposeHandler,
)
from app.app.wallet.port import WalletNotifier
from app.domain.payment.enums import PaymentStatus
from app.domain.wallet.entity import Wallet
from app.domain.wallet.port import WalletRepository
from app.domain.wallet.value_object import WalletId


class ConfirmTopUp(PaymentPurposeHandler):
    def __init__(
        self,
        wallet_repo: WalletRepository,
        notification: TelegramNotification,
        session: DatabaseSession,
        notifier: WalletNotifier,
    ):
        self._wallet_repo: WalletRepository = wallet_repo
        self._notification: TelegramNotification = notification
        self._session: DatabaseSession = session
        self._notifier = notifier

    @override
    async def apply(self, payment: PaymentDTO) -> None:
        if payment.status != PaymentStatus.CONFIRMED:
            return

        wallet: Wallet | None = await self._wallet_repo.acquire(
            wallet_id=WalletId(payment.purpose.reference_id),
        )
        if not wallet:
            raise DataCorruptionError("Wrong wallet_id or wallet don't exists")

        wallet.top_up(
            amount=MoneyMapper.to_value_object(src=payment.original_amount),
        )

    @override
    async def notify(self, payment: PaymentDTO) -> None:
        await self._notifier.notify_top_up(payment=payment)
