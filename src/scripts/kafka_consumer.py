import json
import time
from kafka import KafkaConsumer
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from src.models.sensor.reading import SensorReading, Base
from src.schemas.sensor.reading import SensorReadingCreate, SensorReadingBase

from datetime import datetime
from contextlib import contextmanager
from pydantic import ValidationError

import os
from loguru import logger as logging


# PostgreSQL connection string
DATABASE_URL = "postgresql://postgres-user:postgres-pass@localhost:5432/postgres"

# Kafka settings
KAFKA_TOPIC = "sensor-readings"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9094"

# Create SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)

# Create tables (ensure they exist)
Base.metadata.create_all(bind=engine)

@contextmanager
def get_session():
    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"[DB Error] {e}")
    finally:
        session.close()

def process_message(message_value: str):
    try:
        data = json.loads(message_value)
        # If data is still a string, decode again (handle double-encoded JSON)
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise ValueError("Decoded message is not a dictionary")
        
        validated = SensorReadingCreate(**data)

        db_record = SensorReading(
            timestamp=validated.timestamp,
            machine_id=validated.machine_id,
            temperature=validated.temperature,
            vibration=validated.vibration,
            pressure=validated.pressure,
            power_consumption=validated.power_consumption
        )

        with get_session() as session:
            session.add(db_record)

            logging.info(f"[✓] Saved reading({db_record.id}) for {validated.machine_id} at {validated.timestamp}")

    except ValidationError as e:
        logging.warning(f"[Validation Error] {e}")
    except Exception as e:
        logging.error(f"[Processing Error] {e}")
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],

def run_consumer():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',
        value_deserializer=lambda v: v.decode('utf-8'),
        group_id="sensor-consumer-group"
    )

    logging.info("[Kafka] Listening for messages...")
    for message in consumer:
        # logging.info(f"[Kafka] Received message: {message}")

        process_message(message.value)

if __name__ == "__main__":
    while True:
        try:
            run_consumer()
        except Exception as e:
            logging.error(f"[Consumer Error] {e}")
            time.sleep(5)
