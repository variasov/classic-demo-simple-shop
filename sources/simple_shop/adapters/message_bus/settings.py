from pydantic import BaseSettings


class Settings(BaseSettings):
    BROKER_URL: str
