import json
from confluent_kafka import Consumer, KafkaError


consumer_config = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'order_tracker_group',
    'auto.offset.reset': 'earliest'
}


consumer = Consumer(consumer_config)


consumer.subscribe(['orders'])


print("Consumer is running and subscribed to 'orders' topic...")


try:
    while True:
        msg = consumer.poll(1.0)  # Timeout of 1 second


        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                continue
       
        value = msg.value().decode('utf-8')
        order = json.loads(value)
        print(f"Received message: {msg.value().decode('utf-8')} from topic: {msg.topic()} partition: {msg.partition()} offset: {msg.offset()}")
        print(f"Received Order: {order['quantity']} X {order['item']} from {order['user']} (Order ID: {order['order_id']})")
       
except KeyboardInterrupt:
    print("\nConsumer interrupted by user")
finally:
    consumer.close()



