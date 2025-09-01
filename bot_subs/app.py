import logging

from faststream import FastStream, Logger

from bot_subs.config import settings
from bot_subs.fs_broker import broker
import handlers
# from google_subs.models import db


app = FastStream(
    broker=broker,
)

broker.include_router(handlers.error_router)

@app.on_startup
async def configure_logging() -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
        datefmt=settings.logging.date_format,
    )

# @app.on_startup
# async def create_app(log: Logger) -> None:
#     # await db.initialize()
#     log.critical('FastStream started')

@app.after_startup
async def create_app(log: Logger) -> None:
    log.info('Bot_subs started')

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())