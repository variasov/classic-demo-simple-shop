import logging

from classic.container import container, factory, instance
from classic.messaging.kombu import Publisher, BrokerScheme
from classic.operations import Operation

import kombu
from sqlalchemy.orm import Session

from simple_shop import application
from simple_shop.adapters import database, message_bus, mail_sending, api


container.register(
    application,
    database,
    message_bus,
    mail_sending,
    api,
)


logging.basicConfig(level=logging.INFO)


def new_operation(
    session: Session,
    publisher: Publisher,
):
    return Operation(
        context_managers=session,
        after_complete=publisher.flush,
        on_cancel=publisher.reset,
    )


container.add_settings({
    # DB
    database.Engine: factory(database.engine_from_settings),
    database.Session: factory(database.new_session),

    # MessageBus
    BrokerScheme: instance(message_bus.broker_scheme),
    kombu.Connection: factory(message_bus.connection_from_settings),

    # Application
    Operation: factory(new_operation),

    # API
    api.App: factory(api.App.create),
})
