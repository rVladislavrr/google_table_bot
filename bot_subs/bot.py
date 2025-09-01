__all__ = (
    "bot",
)

from aiogram import Bot

from bot_subs.config import settings

bot = Bot(token=settings.BOT_TOKEN)