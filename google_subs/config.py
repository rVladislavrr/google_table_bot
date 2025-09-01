import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_DEFAULT_FORMAT = (
       "%(levelname)s:     %(asctime)s - %(name)s - %(message)s"
)

BASE_DIR = Path(__file__).parent.parent

class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class Settings(BaseSettings):
    SERVICE_ACCOUNT_FILE: str

    model_config = SettingsConfigDict(env_file=BASE_DIR/".env",
                                      extra="ignore",
                                     )

    @property
    def nats_url(self):
        return 'nats://localhost:4222'

    logging: LoggingConfig = LoggingConfig()


settings = Settings()
