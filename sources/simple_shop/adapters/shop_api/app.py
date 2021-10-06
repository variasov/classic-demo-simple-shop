from classic.http_api import App

from simple_shop.application import services

from .auth import auth
from .join_points import join_points

from . import controllers


def create_app(catalog: services.Catalog,
               checkout: services.Checkout,
               orders: services.Orders) -> App:

    app = App(prefix='/api')

    app.register(controllers.Catalog(catalog=catalog))
    app.register(controllers.Checkout(checkout=checkout))
    app.register(controllers.Orders(orders=orders))

    join_points.join(auth)

    return app
