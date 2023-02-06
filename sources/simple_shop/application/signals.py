from classic.signals import signal


@signal
class CartChanged:
    customer_number: int


@signal
class OrderPlaced:
    order_number: int


@signal
class NewCustomer:
    customer_number: int


@signal
class NewCart:
    customer_number: int
