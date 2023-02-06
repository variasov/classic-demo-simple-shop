from simple_shop.adapters import message_bus

from .container import container


consumer = container.resolve(message_bus.Worker)
consumer.run()
