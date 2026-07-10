import logging
from typing import override

from adaptix import Retort
from aiogram import Bot
from aiogram_dialog import BgManagerFactory, ShowMode
from dishka import AsyncContainer

from app.app.common.port.telegram_notification import (
    Button,
    NotificationRequest,
    TelegramNotification,
)
from app.app.common.port.telegram_notification.dto import DEFAULT_BUTTON
from app.app.order.dto.order import OrderDTO
from app.app.order.port import OrderNotifier
from app.domain.user.value_object import UserId
from app.infra.authentication.telegram.dto import TelegramContextData
from app.infra.authentication.telegram.mapper import TelegramContextMapper
from app.infra.authentication.telegram.port import TelegramContextGateway
from app.presentation.aiogram.port import TranslatorHub
from app.presentation.aiogram.state import OrderState

logger = logging.getLogger(__name__)


class AiogdOrderNotifier(OrderNotifier):
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
    async def notify_confirmed(self, order: OrderDTO) -> None:
        async with self._container() as container:
            gw = await container.get(TelegramContextGateway)
            ctx_data: TelegramContextData | None = await gw.get_data_by_user_id(
                user_id=UserId(order.customer_id)
            )
            if ctx_data is None:
                logger.warning(
                    "No telegram context for user_id=%s", order.customer_id.hex
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
            if context is None or context.state != OrderState.payment:
                await self._send_notification(order)
                return

            dialog_manager.dialog_data["cancel_text"] = text("inl-ui.close")
            dialog_manager.dialog_data["text"] = text(
                "user-shopping-order-payment-confirmed",
                order_id=order.id.hex,
                amount=order.total.amount,
                currency=order.total.currency,
            )
            dialog_manager.dialog_data["to_order_text"] = text(
                "user-shopping-order-payment-confirmed.to-order-btn",
            )
            await dialog_manager.switch_to(state=OrderState.payment_confirmed)
            await dialog_manager.show(show_mode=ShowMode.EDIT)

    async def _send_notification(self, order: OrderDTO) -> None:
        await self._notification.send(
            user_id=UserId(order.customer_id),
            request=NotificationRequest(
                key="order-confirmed-notification",
                buttons=[
                    Button(
                        key="order-confirmed-notification.to-order-btn",
                        data=f"to_order:{order.id}",
                    ),
                    DEFAULT_BUTTON,
                ],
            ),
            order_id=order.id,
            amount=order.total.amount,
            currency=order.total.currency,
        )
