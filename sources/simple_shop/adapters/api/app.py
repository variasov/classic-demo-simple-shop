from classic.components import component
from classic.web import App

from . import controllers


@component
class ShopAPI(App):
    catalog: controllers.Catalog
    checkout: controllers.Checkout
    orders: controllers.Orders

    def __attrs_post_init__(self):
        super().__init__(prefix='/api')

        self.register_controller(self.catalog)
        self.register_controller(self.checkout)
        self.register_controller(self.orders)
