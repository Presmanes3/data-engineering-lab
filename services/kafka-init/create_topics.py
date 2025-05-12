from confluent_kafka.admin import AdminClient, NewTopic

TOPICS = [
    {"name": "sensor-data", "partitions": 3, "replication_factor": 1},
    {"name": "anomaly-alerts", "partitions": 1, "replication_factor": 1},
    {"name": "raw-sensor-logs", "partitions": 3, "replication_factor": 1},
]

admin_config = {
    "bootstrap.servers": "kafka:9092"
}

def create_topics():
    admin_client = AdminClient(admin_config)
    topics_to_create = []

    for topic in TOPICS:
        topics_to_create.append(NewTopic(topic["name"], num_partitions=topic["partitions"],
                                          replication_factor=topic["replication_factor"]))

    futures = admin_client.create_topics(topics_to_create)

    for topic, future in futures.items():
        try:
            future.result()
            print(f"✅ Topic '{topic}' created")
        except Exception as e:
            print(f"⚠️  Failed to create topic '{topic}': {e}")

if __name__ == "__main__":
    create_topics()
