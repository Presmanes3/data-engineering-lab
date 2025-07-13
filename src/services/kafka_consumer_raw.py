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
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection string
POSTGRES_USER = os.getenv("POSTGRESQL_USERNAME")
POSTGRES_PASS = os.getenv("POSTGRESQL_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

if not all([POSTGRES_USER, POSTGRES_PASS, POSTGRES_DB]):
    logging.error("[Config Error] Missing required PostgreSQL environment variables.")
    exit(1)

# Kafka settings
KAFKA_TOPIC = os.getenv("KAFKA_SENSOR_TOPIC")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVER").split(",")

if not KAFKA_TOPIC or not KAFKA_BOOTSTRAP_SERVERS:
    logging.error("[Config Error] KAFKA_SENSOR_TOPIC or KAFKA_SERVER environment variable not set.")
    exit(1)

# Try localhost first, then fallback to 'postgres' (Docker service name)
DATABASE_URLS = [
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@localhost:5432/{POSTGRES_DB}",
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@postgres:5432/{POSTGRES_DB}"
]

def create_engine_with_fallback(urls):
    for url in urls:
        try:
            engine = create_engine(url)
            # Try connecting
            with engine.connect() as conn:
                pass
            logging.info(f"[DB] Connected to {url}")
            return engine
        except OperationalError:
            logging.warning(f"[DB] Could not connect to {url}, trying next...")
    raise RuntimeError("Could not connect to any PostgreSQL server.")

# Create SQLAlchemy engine with fallback
engine = create_engine_with_fallback(DATABASE_URLS)

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

    connected_servers = consumer.config.get('bootstrap_servers')
    logging.info(f"[Kafka] Connected to servers: {connected_servers}")
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
