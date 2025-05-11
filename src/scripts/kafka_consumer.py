from kafka import KafkaConsumer
import time

def run_kafka_consumer():
    while True:  # Infinite loop to ensure the program never ends
        time.sleep(0.001)  # Sleep for a while before starting the consumer
        try:
            # Configure the Kafka consumer
            consumer = KafkaConsumer(
                'your_topic_name',  # Replace with your topic name
                bootstrap_servers=['localhost:9092'],  # Replace with your Kafka broker(s)
                auto_offset_reset='earliest',  # Start reading at the earliest message
                enable_auto_commit=True,
                group_id='your_consumer_group'  # Replace with your consumer group
            )

            print("Kafka Consumer is running...")

            # Consume messages indefinitely
            for message in consumer:
                pass
                # print(f"Received message: {message.value.decode('utf-8')}")
        except Exception as e:
            print(f"Error occurred: {e}. Restarting consumer...")
            time.sleep(5)  # Wait before restarting the consumer
        finally:
            try:
                consumer.close()
            except Exception:
                pass

if __name__ == "__main__":
    run_kafka_consumer()