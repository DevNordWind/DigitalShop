import asyncio
from typing import Final

import uvloop
from aiogram import Bot, Dispatcher
from config.log import LoggingConfig, setup_root_logger
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka
from infra.common.bootstrap import Bootstrap
from infra.framework.sql_alchemy.table import map_all
from infra.framework.taskiq.tp import PriorityBroker
from main.ioc import PROVIDERS
from taskiq import AsyncBroker

_APP_NAME: Final[str] = "bot_polling"


async def main() -> None:
    map_all()

    container: AsyncContainer = make_async_container(*PROVIDERS)
    logging_config: LoggingConfig = await container.get(LoggingConfig)
    setup_root_logger(logging_config, app_name=_APP_NAME)
    bot: Bot = await container.get(Bot)
    dp: Dispatcher = await container.get(Dispatcher)
    _ = await container.get(AsyncBroker)
    __ = await container.get(PriorityBroker)

    async with container() as cont:
        bootstrap: Bootstrap = await cont.get(Bootstrap)
        await bootstrap.check()

    await bot.delete_webhook(drop_pending_updates=True)
    setup_dishka(container, dp)
    return await dp.start_polling(bot)


if __name__ == "__main__":
    from sys import platform

    if platform.startswith("win"):
        asyncio.run(main())
    else:
        uvloop.run(main())
