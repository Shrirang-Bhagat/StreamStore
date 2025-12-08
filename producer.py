import uuid
import json
from confluent_kafka import Producer


producer_config = {
    'bootstrap.servers': 'localhost:9092',
    'message.max.bytes': 1000000000,
    'compression.type': 'gzip',
}


producer = Producer(producer_config)


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed for Order {msg.key()}: {err}")
    else:
        print(f"Order {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
        print(f"Message value: {msg.value().decode('utf-8')}")
        print(dir(msg) )


order = {
    'order_id': str(uuid.uuid4()),
    'user': 'John Doe',
    'item': 'pizza',
    'quantity': 10
}




value = json.dumps(order).encode('utf-8')


producer.produce(
    topic='orders',
    value=value,
    callback=delivery_report)


producer.flush()

