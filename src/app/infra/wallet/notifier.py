import logging
from typing import override

from adaptix import Retort
from aiogram import Bot
from aiogram_dialog import BgManagerFactory, ShowMode
from dishka import AsyncContainer

from app.app.common.port.telegram_notification import (
    NotificationRequest,
    TelegramNotification,
)
from app.app.payment.dto.payment import PaymentDTO
from app.app.wallet.port import WalletNotifier
from app.domain.user.value_object import UserId
from app.infra.authentication.telegram.dto import (
    TelegramContextData,
)
from app.infra.authentication.telegram.mapper import TelegramContextMapper
from app.infra.authentication.telegram.port import TelegramContextGateway
from app.presentation.aiogram.port import TranslatorHub
from app.presentation.aiogram.state import TopUpState

logger = logging.getLogger(__name__)


class AiogdWalletNotifier(WalletNotifier):
    def __init__(
        self,
        bot: Bot,
        bg_manager_factory: BgManagerFactory,
        container: AsyncContainer,
        notification: TelegramNotification,
        retort: Retort,
    ):
        self._container = container
        self._bg_manager_factory = bg_manager_factory
        self._bot = bot
        self._retort = retort
        self._notification = notification

    @override
    async def notify_top_up(self, payment: PaymentDTO) -> None:
        async with self._container() as container:
            gw = await container.get(TelegramContextGateway)
            ctx_data: TelegramContextData | None = await gw.get_data_by_user_id(
                user_id=UserId(payment.creator_id)
            )
            if ctx_data is None:
                logger.warning(
                    "No telegram context for user_id=%s", payment.creator_id.hex
                )
                return

        ctx = TelegramContextMapper.to_dto(src=ctx_data.ctx, role=ctx_data.role)
        t_hub = await self._container.get(TranslatorHub)
        text = t_hub(ctx.lang)

        bg_manager = self._bg_manager_factory.bg(
            bot=self._bot, user_id=ctx.id, chat_id=ctx.id
        )

        async with bg_manager.fg() as dialog_manager:
            context = dialog_manager.current_context()
            if context is None or context.state != TopUpState.payment:
                await self._send_notification(payment)
                return

            dialog_manager.dialog_data["cancel_text"] = text("inl-ui.close")
            dialog_manager.dialog_data["text"] = text(
                "top-up-payment-confirmed",
                amount=payment.original_amount.amount,
                currency=payment.original_amount.currency,
                payment_id=payment.id.hex,
            )
            await dialog_manager.switch_to(state=TopUpState.payment_confirmed)
            await dialog_manager.show(show_mode=ShowMode.EDIT)

    async def _send_notification(self, payment: PaymentDTO) -> None:
        await self._notification.send(
            user_id=UserId(payment.creator_id),
            request=NotificationRequest(key="top-up-notification"),
            amount=payment.original_amount.amount,
            currency=payment.original_amount.currency,
            payment_id=payment.id,
        )
