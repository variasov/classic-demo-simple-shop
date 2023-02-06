from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from .entities import Product, Customer, Cart, Order


class CustomersRepo(ABC):

    @abstractmethod
    def get_by_number(self, number: int) -> Optional[Customer]: ...

    @abstractmethod
    def add(self, customer: Customer): ...

    def get_or_create(self, number: Optional[int]) -> Tuple[Customer, bool]:
        if number is None:
            customer = Customer()
            self.add(customer)
            created = True
        else:
            customer = self.get_by_number(number)
            if customer is None:
                customer = Customer()
                self.add(customer)
                created = True
            else:
                created = False

        return customer, created


class ProductsRepo(ABC):

    @abstractmethod
    def find_by_keywords(self, search: Optional[str] = None,
                         limit: int = 10, offset: int = 0) -> List[Product]: ...

    @abstractmethod
    def get_by_sku(self, sku: str) -> Optional[Product]: ...

    @abstractmethod
    def add(self, product: Product): ...


class CartsRepo(ABC):

    @abstractmethod
    def get_for_customer(self, customer_number: int) -> Optional[Cart]: ...

    @abstractmethod
    def add(self, cart: Cart): ...

    @abstractmethod
    def remove(self, cart: Cart): ...

    def get_or_create(self, customer_number: int) -> Tuple[Cart, bool]:
        cart = self.get_for_customer(customer_number)
        if cart is None:
            cart = Cart(customer_number)
            self.add(cart)
            created = True
        else:
            created = False

        return cart, created


class OrdersRepo(ABC):

    @abstractmethod
    def add(self, order: Order): ...

    @abstractmethod
    def get_by_number(self, number: int) -> Optional[Order]: ...


class MailSender(ABC):

    @abstractmethod
    def send(self, mail: str, title: str, text: str): ...
