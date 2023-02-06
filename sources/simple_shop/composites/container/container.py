import logging

from classic.components import component
from classic.container import container, factory, instance
from classic.messaging.kombu import Publisher, BrokerScheme
from classic.operations import Operation, NewOperation
from classic.signals import Hub

import kombu

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


@component
class AppOperationFactory(NewOperation):
    session: database.Session
    publisher: Publisher
    signals: Hub

    def new(self, **kwargs) -> Operation:
        return Operation(
            on_complete=[
                self.signals.notify_deferred,
                self.session.commit,
                self.publisher.flush,
            ],
            on_cancel=[
                self.session.rollback,
                self.publisher.reset,
                self.signals.reset_deferred,
            ],
            on_finish=[self.session.close],
        )


container.register(AppOperationFactory)

container.add_settings({
    # DB
    database.Engine: factory(database.engine_from_settings),
    database.Session: factory(database.new_session),

    # MessageBus
    BrokerScheme: instance(message_bus.broker_scheme),
    kombu.Connection: factory(message_bus.connection_from_settings),
})
