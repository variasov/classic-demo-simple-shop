from typing import Optional, List, Tuple

from classic.components import component
from classic.aspects import PointCut
from classic.app import DTO, validate_with_dto
from pydantic import validate_arguments

from .dataclasses import Customer, Product, Cart, Order, OrderLine
from .errors import NoProduct, NoOrder, EmptyCart
from . import interfaces


join_points = PointCut()
join_point = join_points.join_point


class ProductInfo(DTO):
    sku: str
    title: str
    description: str
    price: float


class ProductInfoForChange(DTO):
    sku: str
    title: str = None
    description: str = None
    price: float = None


@component
class Catalog:
    products_repo: interfaces.ProductsRepo

    @join_point
    @validate_arguments
    def search_products(self, search: str = None,
                        limit: int = 10, offset: int = 0) -> List[Product]:
        return self.products_repo.find_by_keywords(search, limit, offset)

    @join_point
    @validate_arguments
    def get_product(self, sku: str) -> Product:
        product = self.products_repo.get_by_sku(sku)
        if product is None:
            raise NoProduct(sku=sku)

        return product

    @join_point
    @validate_with_dto
    def add_product(self, product_info: ProductInfo):
        product = product_info.create_obj(Product)
        self.products_repo.add(product)

    @join_point
    @validate_with_dto
    def change_product(self, product_info: ProductInfoForChange):
        product = self.products_repo.get_by_sku(product_info.sku)
        if product is None:
            raise NoProduct(SKU=product_info.sku)

        product_info.populate_obj(product)


@component
class Checkout:
    products_repo: interfaces.ProductsRepo
    customers_repo: interfaces.CustomersRepo
    carts_repo: interfaces.CartsRepo
    orders_repo: interfaces.OrdersRepo

    def _get_customer_and_cart(
        self, customer_id: Optional[int],
    ) -> Tuple[Customer, Cart]:

        customer = self.customers_repo.get_or_create(customer_id)
        cart = self.carts_repo.get_or_create(customer.id)
        return customer, cart

    @join_point
    @validate_arguments
    def get_cart(self, customer_id: int = None) -> Cart:
        __, cart = self._get_customer_and_cart(customer_id)
        return cart

    @join_point
    @validate_arguments
    def add_product_to_cart(self, sku: str,
                            quantity: int = 1,
                            customer_id: int = None):
        product = self.products_repo.get_by_sku(sku)
        if product is None:
            raise NoProduct(sku=sku)

        __, cart = self._get_customer_and_cart(customer_id)
        cart.add_product(product, quantity)

    @join_point
    @validate_arguments
    def remove_product_from_cart(self, sku: str, customer_id: int = None):
        product = self.products_repo.get_by_sku(sku)
        if product is None:
            raise NoProduct(sku=sku)

        __, cart = self._get_customer_and_cart(customer_id)
        cart.remove_product(product)

    @join_point
    @validate_arguments
    def create_order(self, customer_id: int = None) -> int:
        customer, cart = self._get_customer_and_cart(customer_id)
        if cart is None or not cart.positions:
            raise EmptyCart()

        order = Order(customer)

        for position in cart.positions:
            order.lines.append(
                OrderLine(
                    position.product.sku,
                    position.product.title,
                    position.quantity,
                    position.product.price,
                )
            )

        self.orders_repo.add(order)
        self.carts_repo.remove(cart)

        return order.number


@component
class Orders:
    orders_repo: interfaces.OrdersRepo

    @join_point
    @validate_arguments
    def get_order(self, number: int,
                  customer_id: Optional[int] = None) -> Order:

        product = self.orders_repo.get_by_number(number)
        if product is None:
            raise NoOrder(number=number)

        if customer_id and product.customer.id != customer_id:
            raise NoOrder(number=number)

        return product
