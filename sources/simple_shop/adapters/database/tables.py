from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Float, ForeignKey,
)


metadata = MetaData()


customers = Table(
    'customers', metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String),
)

products = Table(
    'products', metadata,
    Column('sku', String, primary_key=True),
    Column('title', String),
    Column('description', String),
    Column('price', Float),
)

carts = Table(
    'carts', metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', ForeignKey('customers.id')),
)

cart_positions = Table(
    'cart_positions', metadata,
    Column('id', Integer, primary_key=True),
    Column('product_sku', ForeignKey('products.sku')),
    Column('cart_id', ForeignKey('carts.id')),
    Column('quantity', Integer),
)

orders = Table(
    'orders', metadata,
    Column('number', Integer, primary_key=True),
    Column('customer_id', ForeignKey('customers.id')),
)

order_lines = Table(
    'order_lines', metadata,
    Column('order_number', ForeignKey('orders.number'), primary_key=True),
    Column('product_sku', String),
    Column('product_title', String),
    Column('price', Float),
    Column('quantity', Integer),
)
