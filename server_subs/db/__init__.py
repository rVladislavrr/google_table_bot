from sqlalchemy.ext.automap import automap_base
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

from server_subs.config import settings


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.engine = None
            self.async_session_maker = None
            self.Base = None
            self._models = {}  # Словарь для хранения моделей
            self._initialized = True

    async def initialize(self):
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=20,
            max_overflow=5,
            pool_timeout=300,
            pool_recycle=1800
        )

        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        self.Base = automap_base()

        async with self.engine.connect() as conn:
            def sync_prepare(connection):
                self.Base.prepare(autoload_with=connection)

            await conn.run_sync(sync_prepare)

        for class_name in self.Base.classes.keys():
            self._models[class_name] = getattr(self.Base.classes, class_name)

    def get_model(self, model_name: str):
        if model_name not in self._models:
            raise ValueError(f"Model {model_name} not found")
        return self._models[model_name]

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session


db = Database()
