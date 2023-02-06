from classic.error_handling import Error


class ShopError(Error):
    namespace = 'shop'


class NoCustomer(ShopError):
    message_template = 'No customer with number "{number}"'


class NoProduct(ShopError):
    message_template = 'No product with SKU "{sku}"'


class NoOrder(ShopError):
    message_template = 'No order with number "{number}"'


class CartIsEmpty(ShopError):
    message_template = 'Cart is empty'


class Some(ShopError):
    code = 'no_product'
