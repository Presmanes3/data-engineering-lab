from kafka import KafkaProducer, KafkaConsumer
import json
import time

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'test-topic'

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send a message
message = {"key": "value", "message": "Hello, Kafka!"}
producer.send(TOPIC_NAME, message)
producer.flush()
print(f"Message sent: {message}")

# Create Kafka consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='test-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Consume messages
print("Waiting for messages...")
for msg in consumer:
    print(f"Received message: {msg.value}")
    break  # Exit after receiving the first message