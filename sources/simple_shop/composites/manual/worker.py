import logging

from classic.persistence.sqlalchemy import TransactionsController
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
    db.metadata.create_all(engine)

    controller = TransactionsController(bind=engine, expire_on_commit=False)

    orders_repo = db.repositories.OrdersRepo(transactions_controller=controller)


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
    orders = services.Orders(
        orders_repo=DB.orders_repo,
        mail_sender=MailSending.sender,
        transactions_controller=DB.controller,
        publisher=MessageBus.publisher,
    )


consumer = message_bus.Worker(
    connection=MessageBus.connection,
    scheme=message_bus.broker_scheme,
    orders=Application.orders,
)

consumer.run()
