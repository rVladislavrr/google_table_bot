__all__ = (
    "broker",
)

from faststream.nats import NatsBroker

from bot_subs.config import settings

broker = NatsBroker(
    settings.nats_url,
)
