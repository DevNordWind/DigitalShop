import asyncio
import secrets
from abc import ABC, abstractmethod
from typing import Any

from aiogram import Bot, Dispatcher, loggers
from aiogram.methods import TelegramMethod
from aiogram.webhook.security import IPFilter
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.responses import JSONResponse


class IpFilterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, ip_filter: IPFilter):
        super().__init__(app=app, dispatch=self.dispatch)
        self._ip_filter: IPFilter = ip_filter

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        ip_address, accept = self._check_ip(request=request)
        if not accept:
            loggers.webhook.warning(
                "Blocking request from an unauthorized IP: %s", ip_address
            )
            return Response(content="Forbidden", status_code=403)
        return await call_next(request)

    def _check_ip(self, request: Request) -> tuple[str, bool]:
        if forwarded_for := request.headers.get("X-Forwarded-For", ""):
            forwarded_for, *_ = forwarded_for.split(",", maxsplit=1)
            return forwarded_for, forwarded_for in self._ip_filter

        # no implementation without reverse proxy
        return "", False


class BaseRequestHandler(ABC):
    def __init__(
        self,
    ) -> None:
        self._background_feed_update_tasks: set[asyncio.Task[Any]] = set()

    @abstractmethod
    def verify_secret(self, telegram_secret_token: str) -> bool:
        raise NotImplementedError

    def register(self, app: FastAPI, /, path: str, **kwargs: Any) -> None:
        router = APIRouter()
        router.add_api_route(
            methods=["POST"], path=path, endpoint=self.handle, **kwargs
        )
        app.include_router(router)

    @inject
    async def handle(
        self,
        request: Request,
        bot: FromDishka[Bot],
        dispatcher: FromDishka[Dispatcher],
    ) -> Response:
        if not self.verify_secret(
            request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        ):
            raise HTTPException(status_code=403, detail="Unauthorized")

        return await self._handle_request_background(
            bot=bot, dispatcher=dispatcher, request=request
        )

    async def close(self) -> None:
        if self._background_feed_update_tasks:
            await asyncio.gather(*self._background_feed_update_tasks)

    async def _background_feed_update(
        self, bot: Bot, dispatcher: Dispatcher, update: dict[str, Any]
    ) -> None:
        result = await dispatcher.feed_raw_update(bot=bot, update=update)

        if isinstance(result, TelegramMethod):
            await dispatcher.silent_call_request(bot=bot, result=result)

    async def _handle_request_background(
        self, bot: Bot, dispatcher: Dispatcher, request: Request
    ) -> Response:
        feed_update_task = asyncio.create_task(
            self._background_feed_update(
                bot=bot,
                dispatcher=dispatcher,
                update=bot.session.json_loads(await request.body()),
            )
        )
        self._background_feed_update_tasks.add(feed_update_task)
        feed_update_task.add_done_callback(
            self._background_feed_update_tasks.discard
        )

        return JSONResponse({})

    __call__ = handle


class SimpleRequestHandler(BaseRequestHandler):
    def __init__(
        self,
        secret: str | None = None,
    ) -> None:
        super().__init__()
        self._secret: str | None = secret

    def verify_secret(self, telegram_secret_token: str) -> bool:
        if self._secret is None:
            return True
        return secrets.compare_digest(telegram_secret_token, self._secret)
