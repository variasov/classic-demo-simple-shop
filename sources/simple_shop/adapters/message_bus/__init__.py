# Добавлено для успешной регистрации
from classic.messaging.kombu import Publisher

from .settings import Settings
from .scheme import broker_scheme
from .consumer import Worker
from .connection import connection_from_settings
