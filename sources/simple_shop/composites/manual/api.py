from sqlalchemy import create_engine

from classic.persistence.sqlalchemy import TransactionsController
from classic.messaging.kombu import KombuPublisher
from kombu import Connection

from simple_shop.application import services
from simple_shop.adapters import database, message_bus, shop_api, mail_sending


class DB:
    db = database

    settings = db.Settings()

    engine = create_engine(settings.DB_URL)
    db.metadata.create_all(engine)

    controller = TransactionsController(bind=engine, expire_on_commit=False)

    customers_repo = db.repositories.CustomersRepo(
        transactions_controller=controller,
    )
    products_repo = db.repositories.ProductsRepo(
        transactions_controller=controller,
    )
    carts_repo = db.repositories.CartsRepo(
        transactions_controller=controller,
    )
    orders_repo = db.repositories.OrdersRepo(
        transactions_controller=controller,
    )


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
    catalog = services.Catalog(
        transactions_controller=DB.controller,
        products_repo=DB.products_repo,
        publisher=MessageBus.publisher,
    )
    checkout = services.Checkout(
        transactions_controller=DB.controller,
        customers_repo=DB.customers_repo,
        products_repo=DB.products_repo,
        carts_repo=DB.carts_repo,
        orders_repo=DB.orders_repo,
        publisher=MessageBus.publisher,
    )
    orders = services.Orders(
        transactions_controller=DB.controller,
        orders_repo=DB.orders_repo,
        mail_sender=MailSending.sender,
        publisher=MessageBus.publisher,
    )


class ShopAPI:
    catalog = shop_api.controllers.Catalog(
        catalog=Application.catalog,
        # transactions_controller=DB.controller,
    )
    checkout = shop_api.controllers.Checkout(
        checkout=Application.checkout,
        # transactions_controller=DB.controller,
    )
    orders = shop_api.controllers.Orders(
        orders=Application.orders,
        # transactions_controller=DB.controller,
    )
    app = shop_api.ShopAPI(
        catalog=catalog,
        checkout=checkout,
        orders=orders,
    )


app = ShopAPI.app


if __name__ == '__main__':
    from werkzeug import run_simple

    run_simple('127.0.0.1', 9000, app)
