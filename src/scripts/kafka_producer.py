from itertools import count
from kafka import KafkaProducer
import json
import time

class KafkaJsonProducer:
    def __init__(self, bootstrap_servers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            batch_size=32768,
            linger_ms=5,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def send_message(self, key, value):
        try:
            self.producer.send(self.topic, key=key.encode('utf-8'), value=value)
            # self.producer.flush()
            # print(f"Message sent to topic {self.topic}: {value}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    def close(self):
        self.producer.close()

if __name__ == "__main__":
    # Configuration
    BOOTSTRAP_SERVERS = ['localhost:9092']
    TOPIC = 'your_topic_name'

    # Initialize producer
    producer = KafkaJsonProducer(BOOTSTRAP_SERVERS, TOPIC)

    # Example usage
    try:
        start_time = time.time()
        counter = 0
        while counter < 10000:
            # time.sleep(0.001)
            producer.send_message(key="key1", value={"message": f"Hello, Kafka! -> {time.time()}", "counter": counter})
            counter += 1
        end_time = time.time()
        print(f"Time taken to send 1000 messages: {end_time - start_time}s")
    finally:
        producer.close()