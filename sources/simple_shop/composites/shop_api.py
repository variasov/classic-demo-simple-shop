from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext

from simple_shop.application import services
from simple_shop.adapters.database import repositories, metadata, DBSettings
from simple_shop.adapters import shop_api


# Secondary adapters

# Database
db_settings = DBSettings()

engine = create_engine(db_settings.DB_URL)
metadata.create_all(engine)

transaction_context = TransactionContext(bind=engine, expire_on_commit=False)

customers_repo = repositories.CustomersRepo(context=transaction_context)
products_repo = repositories.ProductsRepo(context=transaction_context)
carts_repo = repositories.CartsRepo(context=transaction_context)
orders_repo = repositories.OrdersRepo(context=transaction_context)


# Core

catalog = services.Catalog(products_repo=products_repo)
checkout = services.Checkout(
    customers_repo=customers_repo,
    products_repo=products_repo,
    carts_repo=carts_repo,
    orders_repo=orders_repo,
)
orders = services.Orders(orders_repo=orders_repo)


# Primary adapters

# API

app = shop_api.create_app(
    catalog=catalog,
    checkout=checkout,
    orders=orders,
)


# Aspects

services.join_points.join(transaction_context)
shop_api.join_points.join(transaction_context)
