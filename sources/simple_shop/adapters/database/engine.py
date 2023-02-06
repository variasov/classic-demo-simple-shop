from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .settings import Settings


def engine_from_settings(settings: Settings) -> Engine:
    return create_engine(settings.DB_URL)


def new_session(engine: Engine) -> Session:
    factory = sessionmaker(engine, expire_on_commit=False)
    return scoped_session(factory)
