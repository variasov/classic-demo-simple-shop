from simple_shop.adapters import api

from .container import container


api = container.resolve(api.ShopAPI)


if __name__ == '__main__':
    from werkzeug import run_simple

    run_simple('127.0.0.1', 9000, api)
