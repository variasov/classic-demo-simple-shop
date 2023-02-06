from kombu import Connection

from .settings import Settings


def connection_from_settings(settings: Settings) -> Connection:
    return Connection(settings.BROKER_URL)
