from classic.messaging.kombu import KombuConsumer
from classic.components import component

from simple_shop.application import services


@component
class Worker(KombuConsumer):
    orders: services.Orders

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self.register_function(
            self.orders.send_message_to_manager, 'PrintOrderPlaced',
        )
