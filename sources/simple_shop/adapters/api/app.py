from classic.http_api import App as BaseApp

from . import controllers


class App(BaseApp):

    @classmethod
    def create(
        cls,
        catalog: controllers.Catalog,
        checkout: controllers.Checkout,
        orders: controllers.Orders,
    ):

        app = cls(prefix='/api')

        app.register(catalog)
        app.register(checkout)
        app.register(orders)

        return app
