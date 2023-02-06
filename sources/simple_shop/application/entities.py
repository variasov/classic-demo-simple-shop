from typing import Optional, List

from attr import dataclass, field


@dataclass
class Customer:
    id: int
    email: Optional[str] = None
    number: Optional[int] = None


@dataclass
class Product:
    sku: str
    title: str
    description: str
    price: float


@dataclass
class CartPosition:
    product: Product
    quantity: int


@dataclass
class Cart:
    customer_number: int
    positions: List[CartPosition] = field(factory=list)

    def find_position(self, product: Product):
        for position in self.positions:
            if position.product == product:
                return position

    def add_product(self, product: Product, quantity: int):
        position = self.find_position(product)
        if position is None:
            position = CartPosition(product=product, quantity=0)

        position.quantity += quantity

        self.positions.append(position)

    def remove_product(self, product: Product):
        position = self.find_position(product)
        if position is not None:
            self.positions.remove(position)


@dataclass
class OrderLine:
    product_sku: str
    product_title: str
    quantity: int
    price: float


@dataclass
class Order:
    customer: Customer
    number: Optional[int] = None
    lines: List[OrderLine] = field(factory=list)

    @property
    def cost(self):
        return sum((line.price for line in self.lines))
