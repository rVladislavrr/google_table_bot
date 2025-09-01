import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from bot.config import botSettings

from bot.handler.common import router as common_router
from bot.handler.unknown import router as unknown_router
from bot.logger import setup_logging
from bot.middelware import CommandCancelMiddleware
from bot.redis_con import redis_client

log = setup_logging(__name__)


async def start_apps():
    await redis_client.connect()


async def start_bot():
    await start_apps()

    dp.message.middleware(CommandCancelMiddleware())
    dp.include_router(common_router)
    dp.include_router(unknown_router)
    log.info('Starting bot')
    try:
        await dp.start_polling(bot)
    finally:
        log.info('Stopping bot')


if __name__ == '__main__':
    bot = Bot(token=botSettings.TOKEN)

    ## редиса может и не быть
    storage = RedisStorage.from_url(botSettings.REDIS_BASE_URL + '/5')

    dp = Dispatcher(storage=storage)
    asyncio.run(start_bot())
