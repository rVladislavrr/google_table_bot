__all__ = (
    "broker",
)

from faststream.nats import NatsBroker

from bot.config import botSettings

broker = NatsBroker(
    botSettings.nats_url,
)
