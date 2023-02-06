from classic.components import component
from classic.web import Request, Response, get, post, cache_control
from classic.operations import operation

from simple_shop.application import services

from .auth import auth


@component
class Catalog:
    catalog: services.Catalog
    
    @get
    @cache_control
    def show_product(self, request: Request) -> Response:
        product = self.catalog.get_product(**request.args)
        return Response({
            'sku': product.sku,
            'title': product.title,
            'description': product.description,
            'price': product.price,
        })
    
    @get
    @cache_control
    @operation
    def search_product(self, request: Request) -> Response:
        products = self.catalog.search_products(**request.args)
        return Response([
            {
                'sku': product.sku,
                'title': product.title,
                'description': product.description,
                'price': product.price,
            } for product in products
        ])


@component
class Checkout:
    checkout: services.Checkout

    @auth
    @get
    @operation
    def show_cart(self, request: Request) -> Response:
        cart = self.checkout.get_cart(customer_number=request.context.client_id)
        return Response({
            'positions': [
                {
                    'product_sku': position.product.sku,
                    'product_price': position.product.price,
                    'quantity': position.quantity,
                }
                for position in cart.positions
            ]
        })

    @auth
    @post
    def add_product_to_cart(self, request: Request) -> Response:
        self.checkout.add_product_to_cart(
            customer_id=request.context.client_id,
            **(request.json or {}),
        )
        return Response()

    @auth
    @post
    def remove_product_from_cart(self, request: Request) -> Response:
        self.checkout.remove_product_from_cart(
            customer_id=request.context.client_id,
            **request.json,
        )
        return Response()

    @auth
    @post
    def register_order(self, request: Request) -> Response:
        order_number = self.checkout.create_order(
            customer_id=request.context.client_id,
        )
        return Response({'order_number': order_number})


@component
class Orders:
    orders: services.Orders

    @auth
    @get
    @cache_control
    def show_order(self, request: Request) -> Response:
        order = self.orders.get_order(
            customer_id=request.context.client_id,
            **request.json,
        )
        return Response({
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
        })
