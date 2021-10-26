from classic.messaging_kombu import BrokerScheme
from kombu import Exchange, Queue


broker_scheme = BrokerScheme(
    Queue('PrintOrderPlaced', Exchange('OrderPlaced'), max_length=1)
)
