from abc import ABC, abstractmethod
from typing import Optional, List

from .dataclasses import Product, Customer, Cart, Order


class CustomersRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[Customer]: ...

    @abstractmethod
    def add(self, customer: Customer): ...

    def get_or_create(self, id_: Optional[int]) -> Customer:
        if id_ is None:
            customer = Customer()
            self.add(customer)
        else:
            customer = self.get_by_id(id_)
            if customer is None:
                customer = Customer()
                self.add(customer)

        return customer


class ProductsRepo(ABC):

    @abstractmethod
    def find_by_keywords(self, search: str = None,
                         limit: int = 10,
                         offset: int = 0) -> List[Product]: ...

    @abstractmethod
    def get_by_sku(self, sku: str) -> Optional[Product]: ...

    @abstractmethod
    def add(self, product: Product): ...


class CartsRepo(ABC):

    @abstractmethod
    def get_for_customer(self, customer_id: int) -> Optional[Cart]: ...

    @abstractmethod
    def add(self, cart: Cart): ...

    @abstractmethod
    def remove(self, cart: Cart): ...

    def get_or_create(self, customer_id: int) -> Cart:
        cart = self.get_for_customer(customer_id)
        if cart is None:
            cart = Cart(customer_id)
            self.add(cart)

        return cart


class OrdersRepo(ABC):

    @abstractmethod
    def add(self, order: Order): ...

    @abstractmethod
    def get_by_number(self, number: int) -> Optional[Order]: ...


class MailSender(ABC):

    @abstractmethod
    def send(self, mail: str, title: str, text: str): ...
