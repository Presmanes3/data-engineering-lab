import json
import random
import time

from typing import List

import datetime
from kafka import KafkaProducer
from pydantic import ValidationError

from src.schemas.sensor.reading import SensorReadingCreate, SensorReadingBase  # Usa tu modelo

from src.controller.sensor.temperature.generator import TemperatureSensorGenerator
from src.schemas.sensor.temperature.sensor_configuration import TemperatureConfiguration

from src.controller.sensor.producer import SensorProducer

from loguru import logger as logging
from dotenv import load_dotenv
import os


load_dotenv()

KAFKA_TOPIC = os.getenv("KAFKA_SENSOR_TOPIC")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVER").split(",")

if not KAFKA_TOPIC or not KAFKA_BOOTSTRAP_SERVERS:
    logging.error("KAFKA_SENSOR_TOPIC or KAFKA_SERVER environment variable not set.")
    exit(1)


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_data_to_kafka(reading: SensorReadingBase):
    try:
        producer.send(KAFKA_TOPIC, value=reading.model_dump_json())
        producer.flush(1)  # Espera a que el mensaje se envíe
        logging.info(f"[✓] Sent reading for {reading.machine_id} at {reading.timestamp}")
    except ValidationError as e:
        logging.warning(f"[Validation Error] {e}")


def run_producer():
    logging.info("[Kafka Producer] Starting to send messages...")

    temperature_1_configuration = TemperatureConfiguration(
        ranges={
            "early_morning": (15.0, 2.0),
            "midday": (25.0, 1.5),
            "evening": (20.0, 1.0)
        }
    )

    temperature_2_configuration = TemperatureConfiguration(
        ranges={
            "early_morning": (16.0, 1.5),
            "midday": (26.0, 2.0),
            "evening": (21.0, 1.2)
        }
    )

    temperature_1_generator = TemperatureSensorGenerator(
        config=temperature_1_configuration
    )

    temperature_2_generator = TemperatureSensorGenerator(
        config=temperature_2_configuration
    )

    machine_1 = SensorProducer(
        machine_id              = "machine_1",
        temperature_generator   = temperature_1_generator
    )
    machine_2 = SensorProducer(
        machine_id              = "machine_2",
        temperature_generator   = temperature_2_generator
    )

    machine_1_production : List[SensorReadingBase] = machine_1.generate_readings(start_hour=6, end_hour=20, interval_seconds=60, date=datetime.date.today())
    machine_2_production : List[SensorReadingBase] = machine_2.generate_readings(start_hour=6, end_hour=20, interval_seconds=60, date=datetime.date.today())

    for reading in machine_1_production + machine_2_production:
        send_data_to_kafka(reading)

    producer.flush(2)
        
if __name__ == "__main__":
    # 1. Check if Kafka is running (enviando un mensaje de prueba)
    try:
        # Enviar un mensaje de prueba (no se almacenará, solo para probar la conexión)
        future = producer.send(KAFKA_TOPIC, value=json.dumps({"test": "connection"}))
        future.get(timeout=10)
        logging.info("[Kafka] Connection successful")
    except Exception as e:
        logging.error(f"[Kafka] Connection failed: {e}")
        exit(1)


    run_producer()
