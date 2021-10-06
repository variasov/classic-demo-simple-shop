from typing import Optional, List

import attr


@attr.dataclass
class Customer:
    id: Optional[int] = None
    email: Optional[str] = None


@attr.dataclass
class Product:
    sku: str
    title: str
    description: str
    price: float


@attr.dataclass
class CartPosition:
    product: Product
    quantity: int


@attr.dataclass
class Cart:
    customer_id: int
    positions: List[CartPosition] = attr.ib(factory=list)

    def find_position(self, product: Product):
        for position in self.positions:
            if position.product == product:
                return position

    def add_product(self, product: Product, quantity: int):
        position = self.find_position(product)
        if position is None:
            position = CartPosition(product, 0)

        position.quantity += quantity

        self.positions.append(position)

    def remove_product(self, product: Product):
        position = self.find_position(product)
        if position is not None:
            self.positions.remove(position)


@attr.dataclass
class OrderLine:
    product_sku: str
    product_title: str
    quantity: int
    price: float


@attr.dataclass
class Order:
    customer: Customer
    number: Optional[int] = None
    lines: List[OrderLine] = attr.ib(factory=list)