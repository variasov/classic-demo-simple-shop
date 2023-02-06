import kombu
from sqlalchemy import engine

from simple_shop.adapters import database, message_bus

from .container import container


# Database
db_engine = container.resolve(engine.Engine)
database.metadata.create_all(db_engine)


# Message Bus
connection = container.resolve(kombu.Connection)
message_bus.broker_scheme.declare(connection)
