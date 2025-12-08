# StreamStore# StreamStore


A simple Apache Kafka streaming application demonstrating producer-consumer pattern for order processing using Python and Docker.


## Overview


StreamStore is a Kafka-based message streaming application that simulates an order processing system. It consists of a Kafka broker running in Docker and Python applications that produce and consume order messages.


## Architecture


```
┌─────────────────────────────────────────────────────────────────┐
│                        StreamStore System                       │
└─────────────────────────────────────────────────────────────────┘


    ┌──────────────────┐                    ┌──────────────────┐
    │  producer.py     │                    │   tracker.py     │
    │  (Producer)      │                    │   (Consumer)     │
    └────────┬─────────┘                    └────────▲─────────┘
             │                                       │
             │ Produces Messages                     │ Consumes Messages
             │ (JSON Orders)                         │ (JSON Orders)
             │                                       │
             ▼                                       │
    ┌────────────────────────────────────────────────────────────┐
    │           Kafka Broker (KRaft Mode)                        │
    │                                                            │
    │  ┌──────────────────────────────────────────────────┐      │
    │  │         Topic: orders                            │      │
    │  │  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐      │      │
    │  │  │ Msg 0 │  │ Msg 1 │  │ Msg 2 │  │ Msg 3 │...   │      │
    │  │  └───────┘  └───────┘  └───────┘  └───────┘      │      │
    │  │         Partition: 0                             │      │
    │  └──────────────────────────────────────────────────┘      │
    │                                                            │
    │  Consumer Group: order_tracker_group                       │
    │  ├─ Offset Tracking                                        │
    │  └─ Message Retention                                      │
    │                                                            │
    │  Configuration:                                            │
    │  • Port: 9092                                              │
    │  • Max Message Size: 2GB                                   │
    │  • Replication Factor: 1                                   │
    │  • Compression: GZIP                                       │
    └────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Docker Volume  │
                    │  kafka_kraft    │
                    │  (Persistence)  │
                    └─────────────────┘
```


### Component Details


- **Kafka Broker**: Apache Kafka 7.8.3 running in KRaft mode (single-node cluster)
- **Producer**: Python application that generates and publishes order messages to Kafka
- **Consumer/Tracker**: Python application that subscribes to and processes order messages from Kafka


## Features


- **Docker-based Kafka setup** using KRaft mode (no Zookeeper required)
- **Producer application** that sends order messages with:
  - Unique order IDs (UUID)
  - Customer information
  - Item details and quantity
  - Delivery confirmation callbacks
  - GZIP compression for efficient message transfer
- **Consumer application** that:
  - Subscribes to the `orders` topic
  - Polls for messages continuously
  - Processes and displays order information
  - Handles errors gracefully
- **Support for large messages** (up to 1GB on client, 2GB on broker)


## Prerequisites


- Docker and Docker Compose
- Python 3.7+
- pip (Python package manager)


## Installation


1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StreamStore
   ```


2. **Install Python dependencies**
   ```bash
   pip install -r requirments.txt
   ```


3. **Start Kafka broker**
   ```bash
   docker-compose up -d
   ```


4. **Create the orders topic** (if not auto-created)
   ```bash
   docker exec kafka_server kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1
   ```


## Usage


### Running the Producer


Send order messages to Kafka:


```bash
python producer.py
```


This will create and send a sample order message to the `orders` topic with delivery confirmation.


### Running the Consumer/Tracker


Listen for and process order messages:


```bash
python tracker.py
```


The tracker will:
- Connect to Kafka
- Subscribe to the `orders` topic
- Display received orders in real-time
- Continue running until interrupted (Ctrl+C)


### Example Output


**Producer:**
```
Order None successfully produced to orders [0] at offset 0
Message value: {"order_id": "123e4567-e89b-12d3-a456-426614174000", "user": "John Doe", "item": "pizza", "quantity": 10}
```


**Consumer:**
```
Consumer is running and subscribed to 'orders' topic...
Received message: {"order_id": "123e4567-e89b-12d3-a456-426614174000", "user": "John Doe", "item": "pizza", "quantity": 10} from topic: orders partition: 0 offset: 0
Received Order: 10 X pizza from John Doe (Order ID: 123e4567-e89b-12d3-a456-426614174000)
```


## Configuration


### Kafka Broker (docker-compose.yaml)


- **Port**: 9092 (exposed on localhost)
- **Mode**: KRaft (Kafka Raft) - no Zookeeper required
- **Replication Factor**: 1 (single broker setup)
- **Max Message Size**: 2GB (broker), 1GB (client)
- **Compression**: Enabled (producer uses GZIP)


### Producer Configuration


- **Bootstrap Servers**: localhost:9092
- **Max Message Size**: 1,000,000,000 bytes (1GB)
- **Compression**: GZIP


### Consumer Configuration


- **Bootstrap Servers**: localhost:9092
- **Consumer Group**: order_tracker_group
- **Auto Offset Reset**: earliest (start from beginning if no offset)
- **Poll Timeout**: 1 second


## Project Structure


```
StreamStore/
├── docker-compose.yaml    # Kafka broker configuration
├── producer.py           # Order producer application
├── tracker.py            # Order consumer application
├── requirments.txt       # Python dependencies
├── README.md            # Project documentation
└── my_work.txt          # Additional notes
```


## Troubleshooting


### Kafka broker not starting
```bash
docker-compose down
docker volume rm streamstore_kafka_kraft
docker-compose up -d
```


### Topic not found
Create the topic manually:
```bash
docker exec kafka_server kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1
```


### List all topics
```bash
docker exec kafka_server kafka-topics --bootstrap-server localhost:9092 --list
```


### View consumer groups
```bash
docker exec kafka_server kafka-consumer-groups --bootstrap-server localhost:9092 --list
```


### Check Kafka logs
```bash
docker logs kafka_server
```


## Dependencies


- **confluent-kafka**: Python client for Apache Kafka


## Notes


- This is a development setup with a single Kafka broker
- For production use, configure multiple brokers and appropriate replication factors
- Large message support (>1GB) is configured but consider using external storage (S3, etc.) for very large payloads
- The setup uses KRaft mode, which is the future of Kafka (Zookeeper-less)







