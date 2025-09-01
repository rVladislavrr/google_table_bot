from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class BotSettings(BaseSettings):
    TOKEN: str
    EMAIL: str
    SERVER_URL: str

    REDIS_USER_PASSWORD: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    @property
    def REDIS_BASE_URL(self) -> str:
        return f"redis://:{self.REDIS_USER_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def nats_url(self):
        return 'nats://localhost:4222'

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env",
                                      extra="ignore", env_prefix="BOT_")


botSettings = BotSettings()
