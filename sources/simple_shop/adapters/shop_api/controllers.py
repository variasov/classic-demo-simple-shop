from classic.components import component

from simple_shop.application import services

from .join_points import join_point


@component
class Catalog:
    catalog: services.Catalog

    @join_point
    def on_get_show_product(self, request, response):
        product = self.catalog.get_product(**request.params)
        response.media = {
            'sku': product.sku,
            'title': product.title,
            'description': product.description,
            'price': product.price,
        }

    @join_point
    def on_get_search_product(self, request, response):
        products = self.catalog.search_products(**request.params)
        response.media = [
            {
                'sku': product.sku,
                'title': product.title,
                'description': product.description,
                'price': product.price,
            } for product in products
        ]


@component
class Checkout:
    checkout: services.Checkout

    @join_point
    def on_get_show_cart(self, request, response):
        cart = self.checkout.get_cart(request.context.client_id)
        response.media = {
            'positions': [
                {
                    'product_sku': position.product.sku,
                    'product_price': position.product.price,
                    'quantity': position.quantity,
                }
                for position in cart.positions
            ]
        }

    @join_point
    def on_post_add_product_to_cart(self, request, response):
        self.checkout.add_product_to_cart(
            customer_id=request.context.client_id,
            **request.media,
        )

    @join_point
    def on_post_remove_product_from_cart(self, request, response):
        self.checkout.remove_product_from_cart(
            customer_id=request.context.client_id,
            **request.media,
        )

    @join_point
    def on_post_register_order(self, request, response):
        order_number = self.checkout.create_order(
            customer_id=request.context.client_id,
        )
        response.media = {'order_number': order_number}


@component
class Orders:
    orders: services.Orders

    @join_point
    def on_get_show_order(self, request, response):
        order = self.orders.get_order(
            customer_id=request.context.client_id,
            **request.params,
        )
        response.media = {
            'number': order.number,
            'positions': [
                {
                    'sku': line.product_sku,
                    'product_title': line.product_title,
                    'quantity': line.quantity,
                    'price': line.price,
                }
                for line in order.lines
            ]
        }
