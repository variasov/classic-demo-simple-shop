from typing import Optional, List

from classic.components import component
from sqlalchemy import select
from sqlalchemy.orm import Session

from simple_shop.application import interfaces
from simple_shop.application.entities import Customer, Product, Order, Cart


@component
class CustomersRepo(interfaces.CustomersRepo):
    session: Session

    def get_by_number(self, number: int) -> Optional[Customer]:
        query = select(Customer).where(Customer.number == number)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, customer: Customer):
        self.session.add(customer)
        self.session.flush()


@component
class ProductsRepo(interfaces.ProductsRepo):
    session: Session

    def find_by_keywords(self, search: str = '',
                         limit: int = 10,
                         offset: int = 0) -> List[Product]:

        query = (select(Product).order_by(Product.sku)
                                .limit(limit)
                                .offset(offset))

        if search is not None:
            query = query.where(
                Product.title.ilike(f'%{search}%') |
                Product.description.ilike(f'%{search}%')
            )

        return self.session.execute(query).scalars()

    def get_by_sku(self, sku: str) -> Optional[Product]:
        query = select(Product).where(Product.sku == sku)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, product: Product):
        self.session.add(product)
        self.session.flush()


@component
class CartsRepo(interfaces.CartsRepo):
    session: Session

    def get_for_customer(self, customer_number: int) -> Optional[Cart]:
        query = select(Cart).where(Cart.customer_number == customer_number)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, cart: Cart):
        self.session.add(cart)
        self.session.flush()

    def remove(self, cart: Cart):
        self.session.delete(cart)


@component
class OrdersRepo(interfaces.OrdersRepo):
    session: Session

    def get_by_number(self, number: int) -> Optional[Order]:
        query = select(Order).where(Order.number == number)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, order: Order):
        self.session.add(order)
        self.session.flush()
