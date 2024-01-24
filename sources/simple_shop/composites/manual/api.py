from sqlalchemy import create_engine

from classic.operations import Operation
from classic.messaging.kombu import KombuPublisher
from kombu import Connection

from simple_shop.application import services
from simple_shop.adapters import database, message_bus, api, mail_sending


class DB:
    db = database

    settings = db.Settings()
    engine = create_engine(settings.DB_URL)
    session = db.new_session(engine)

    customers_repo = db.repositories.CustomersRepo(session=session)
    products_repo = db.repositories.ProductsRepo(session=session)
    carts_repo = db.repositories.CartsRepo(session=session)
    orders_repo = db.repositories.OrdersRepo(session=session)


class MessageBus:
    settings = message_bus.Settings()
    connection = Connection(settings.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


class MailSending:
    sender = mail_sending.LogMailSender()


class Application:
    operation = Operation(
        context_managers=DB.session,
        after_complete=MessageBus.publisher.flush,
        on_cancel=MessageBus.publisher.reset,
    )
    catalog = services.Catalog(
        operaion_=operation,
        products_repo=DB.products_repo,
        publisher=MessageBus.publisher,
    )
    checkout = services.Checkout(
        operaion_=operation,
        customers_repo=DB.customers_repo,
        products_repo=DB.products_repo,
        carts_repo=DB.carts_repo,
        orders_repo=DB.orders_repo,
        publisher=MessageBus.publisher,
    )
    orders = services.Orders(
        operaion_=operation,
        orders_repo=DB.orders_repo,
        mail_sender=MailSending.sender,
        publisher=MessageBus.publisher,
    )


class API:
    catalog = api.controllers.Catalog(
        catalog=Application.catalog,
    )
    checkout = api.controllers.Checkout(
        checkout=Application.checkout,
    )
    orders = api.controllers.Orders(
        orders=Application.orders,
    )
    app = api.App.create(
        catalog=catalog,
        checkout=checkout,
        orders=orders,
    )


app = API.app


if __name__ == '__main__':
    from werkzeug import run_simple

    run_simple('127.0.0.1', 9000, app)
