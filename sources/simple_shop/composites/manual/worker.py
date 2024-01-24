import logging

from classic.operations import Operation
from classic.messaging.kombu import KombuPublisher

from sqlalchemy import create_engine
from kombu import Connection

from simple_shop.application import services
from simple_shop.adapters import database, message_bus, mail_sending


logging.basicConfig(level=logging.INFO)


class DB:
    db = database

    settings = db.Settings()
    engine = create_engine(settings.DB_URL)
    session = db.new_session(engine)

    orders_repo = db.repositories.OrdersRepo(session=session)


class MailSending:
    sender = mail_sending.LogMailSender()


class MessageBus:
    settings = message_bus.Settings()
    connection = Connection(settings.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


class Application:
    operation = Operation(
        context_managers=DB.session,
        after_complete=MessageBus.publisher.flush,
        on_cancel=MessageBus.publisher.reset,
    )
    orders = services.Orders(
        orders_repo=DB.orders_repo,
        mail_sender=MailSending.sender,
        operation_=operation,
        publisher=MessageBus.publisher,
    )


consumer = message_bus.Worker(
    connection=MessageBus.connection,
    scheme=message_bus.broker_scheme,
    orders=Application.orders,
)

consumer.run()
