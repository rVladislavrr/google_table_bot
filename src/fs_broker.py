__all__ = (
    "broker",
)

from faststream.nats import NatsBroker

from src.config import settings

broker = NatsBroker(
    settings.nats_url,
)
