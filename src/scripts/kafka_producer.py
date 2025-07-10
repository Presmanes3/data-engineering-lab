import json
import random
import time

from datetime import datetime
from kafka import KafkaProducer
from pydantic import ValidationError
from src.schemas.sensor.reading import SensorReadingCreate, SensorReadingBase  # Usa tu modelo

from loguru import logger as logging

KAFKA_TOPIC = "sensor-readings"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9094"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_sensor_data() -> SensorReadingBase:
    return SensorReadingBase(
        timestamp=datetime.utcnow().isoformat(),
        machine_id=f"machine_{random.randint(1, 3)}",
        temperature=round(random.uniform(50, 100), 2),
        vibration=round(random.uniform(0.1, 5.0), 2),
        pressure=round(random.uniform(2.0, 10.0), 2),
        power_consumption=round(random.uniform(1000, 5000), 2)
    )

def run_producer():
    logging.info("[Kafka Producer] Starting to send messages...")
    while True:
        payload = generate_sensor_data()
        try:
            
            producer.send(KAFKA_TOPIC, value=payload.model_dump_json())
            logging.info(f"[✓] Sent reading for {payload.machine_id}")
        except ValidationError as e:
            logging.warning(f"[Validation Error] {e}")
        time.sleep(2)

if __name__ == "__main__":
    run_producer()
