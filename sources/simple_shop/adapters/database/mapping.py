from sqlalchemy.orm import registry, relationship

from simple_shop.application import dataclasses

from . import tables


mapper = registry()

mapper.map_imperatively(dataclasses.Customer, tables.customers)

mapper.map_imperatively(dataclasses.Product, tables.products)

mapper.map_imperatively(
    dataclasses.CartPosition,
    tables.cart_positions,
    properties={
        'product': relationship(dataclasses.Product,
                                uselist=False, lazy='joined')
    }
)

mapper.map_imperatively(dataclasses.Cart, tables.carts, properties={
    'positions': relationship(
        dataclasses.CartPosition, lazy='subquery',
    )
})

mapper.map_imperatively(dataclasses.OrderLine, tables.order_lines)

mapper.map_imperatively(dataclasses.Order, tables.orders, properties={
    'lines': relationship(dataclasses.OrderLine, lazy='subquery'),
    'customer': relationship(dataclasses.Customer,
                             uselist=False, lazy='joined'),
})
