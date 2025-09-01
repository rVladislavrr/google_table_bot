import logging

from faststream import FastStream, Logger

from server_subs.config import settings
from server_subs.db import db
from server_subs.fs_broker import broker
from handlers.users import router as user_router

app = FastStream(
    broker=broker,
)

broker.include_router(user_router)

@app.on_startup
async def configure_logging() -> None:
    await db.initialize()
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
        datefmt=settings.logging.date_format,
    )

@app.after_startup
async def create_app(log: Logger) -> None:

    log.info('server_subs started')


if __name__ == "__main__":
    import asyncio

    asyncio.run(app.run())
