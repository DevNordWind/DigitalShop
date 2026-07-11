import asyncio

import uvloop
from aiogram import Bot, Dispatcher
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka

from app.config import LoggingConfig
from app.infra.common.bootstrap import Bootstrap
from app.infra.framework.sql_alchemy.table import map_all
from app.main.ioc import PROVIDERS
from app.main.ioc.presentation import (
    AiogramAdaptersProvider,
    TelegramAuthenticationHandlersProvider,
)


async def main() -> None:
    map_all()

    container: AsyncContainer = make_async_container(
        *(
            *PROVIDERS,
            AiogramAdaptersProvider(),
            TelegramAuthenticationHandlersProvider(),
        )
    )
    logging_config: LoggingConfig = await container.get(LoggingConfig)
    logging_config.setup_logging()
    bot: Bot = await container.get(Bot)
    dp: Dispatcher = await container.get(Dispatcher)

    async with container() as cont:
        bootstrap: Bootstrap = await cont.get(Bootstrap)
        await bootstrap.startup()

    await bot.delete_webhook(drop_pending_updates=True)
    setup_dishka(container, dp)
    return await dp.start_polling(bot)


if __name__ == "__main__":
    from sys import platform

    if platform.startswith("win"):
        asyncio.run(main())
    else:
        uvloop.run(main())
