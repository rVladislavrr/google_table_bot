from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from src.api.v1 import router
from src.fs_broker import broker
from src.logger import setup_logging
from src.middlewares.log_middle import LoggingMiddleware

log = setup_logging('main')

@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    log.info("Сервер старт")
    yield
    await broker.stop()
    log.info("Сервер стоп")
app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix='/api')

app.add_middleware(LoggingMiddleware)