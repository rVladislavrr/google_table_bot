import logging

from faststream import FastStream, Logger

from google_subs.config import settings
from google_subs.fs_broker import broker
from google_subs.handlers.users import router as users_router


app = FastStream(
    broker=broker,
)

broker.include_router(users_router)

@app.on_startup
async def configure_logging() -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
        datefmt=settings.logging.date_format,
    )

@app.after_startup
async def create_app(log: Logger) -> None:
    log.info('google_subs started')

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())