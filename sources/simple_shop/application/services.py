from typing import Optional, List, Tuple

from classic.components import component
from classic.validation import ValidationModel
from classic.signals import Hub, reaction
from classic.operations import operation

from .entities import Customer, Product, Cart, Order, OrderLine

from . import interfaces, signals, errors


class ProductInfo(ValidationModel):
    sku: str
    title: str
    description: str
    price: float


class ProductInfoForChange(ValidationModel):
    sku: str
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


@component
class Catalog:
    products: interfaces.ProductsRepo

    @operation
    def search_products(self, search: str = None,
                        limit: int = 10, offset: int = 0) -> List[Product]:
        return list(self.products.find_by_keywords(search, limit, offset))

    @operation
    def get_product(self, sku: str) -> Product:
        product = self.products.get_by_sku(sku)
        if product is None:
            raise errors.NoProduct(sku=sku)

        return product

    @operation
    def add_product(self, product_info: ProductInfo):
        product = product_info.create_obj(Product)
        self.products.add(product)

    @operation
    def change_product(self, product_info: ProductInfoForChange):
        product = self.products.get_by_sku(product_info.sku)
        if product is None:
            raise errors.NoProduct(SKU=product_info.sku)

        product_info.populate_obj(product)


@component
class Checkout:
    products: interfaces.ProductsRepo
    customers: interfaces.CustomersRepo
    carts: interfaces.CartsRepo
    orders: interfaces.OrdersRepo
    signals: Hub

    def _get_customer_and_cart(
        self, customer_number: Optional[int],
    ) -> Tuple[Customer, Cart]:

        customer, created = self.customers.get_or_create(customer_number)
        if created:
            self.signals.notify(
                signals.NewCustomer(customer_number)
            )
        cart, created = self.carts.get_or_create(customer.number)
        if created:
            self.signals.notify(
                signals.NewCart(customer.number)
            )
        return customer, cart

    @operation
    def get_cart(self, customer_number: int = None) -> Cart:
        __, cart = self._get_customer_and_cart(customer_number)
        return cart

    @operation
    def add_product_to_cart(self, sku: str,
                            quantity: int = 1,
                            customer_id: int = None):
        product = self.products.get_by_sku(sku)
        if product is None:
            raise errors.NoProduct(sku=sku)

        __, cart = self._get_customer_and_cart(customer_id)
        cart.add_product(product, quantity)

        self.signals.notify(
            signals.CartChanged(cart.customer_number)
        )

    @operation
    def remove_product_from_cart(self, sku: str, customer_id: int = None):
        product = self.products.get_by_sku(sku)
        if product is None:
            raise errors.NoProduct(sku=sku)

        __, cart = self._get_customer_and_cart(customer_id)
        cart.remove_product(product)

    @operation
    def create_order(self, customer_id: int = None) -> int:
        customer, cart = self._get_customer_and_cart(customer_id)
        if cart is None or not cart.positions:
            raise errors.CartIsEmpty

        order = Order(
            customer,
            lines=[
                OrderLine(
                    position.product.sku,
                    position.product.title,
                    position.quantity,
                    position.product.price
                ) for position in cart.positions
            ]
        )

        self.orders.add(order)
        self.carts.remove(cart)

        self.signals.notify(
            signals.OrderPlaced(order.number)
        )

        return order.number


@component
class Orders:
    orders: interfaces.OrdersRepo
    mail_sender: interfaces.MailSender

    @operation
    def get_order(self, number: int,
                  customer_id: Optional[int] = None) -> Order:

        order = self.orders.get_by_number(number)
        if order is None:
            raise errors.NoOrder(number=number)

        if customer_id and order.customer.id != customer_id:
            raise errors.NoOrder(number=number)

        return order

    @reaction
    def send_message_to_manager(self, signal: signals.OrderPlaced):
        order = self.orders.get_by_number(signal.order_number)
        if order is None:
            raise errors.NoOrder(number=signal.order_number)

        self.mail_sender.send(
            'admin@example.com',
            'New order placed!',
            f'Order with number {order.number} and cost {order.cost} '
            f'have been created and waiting for approve.'
        )
