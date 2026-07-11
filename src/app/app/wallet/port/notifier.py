from abc import ABC, abstractmethod

from app.app.payment.dto.payment import PaymentDTO


class WalletNotifier(ABC):
    @abstractmethod
    async def notify_top_up(self, payment: PaymentDTO) -> None:
        raise NotImplementedError
