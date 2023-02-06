from sqlalchemy.orm import registry, relationship

from simple_shop.application import entities

from . import tables


mapper = registry()

mapper.map_imperatively(entities.Customer, tables.customers)

mapper.map_imperatively(entities.Product, tables.products)

mapper.map_imperatively(
    entities.CartPosition,
    tables.cart_positions,
    properties={
        'product': relationship(entities.Product, uselist=False, lazy='joined')
    }
)

mapper.map_imperatively(entities.Cart, tables.carts, properties={
    'positions': relationship(
        entities.CartPosition, lazy='subquery',
    )
})

mapper.map_imperatively(entities.OrderLine, tables.order_lines)

mapper.map_imperatively(entities.Order, tables.orders, properties={
    'lines': relationship(entities.OrderLine, lazy='subquery'),
    'customer': relationship(entities.Customer, uselist=False, lazy='joined'),
})
