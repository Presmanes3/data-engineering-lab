import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    machine_id = Column(String, nullable=False, index=True)
    temperature = Column(Float, nullable=True)
    vibration = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    power_consumption = Column(Float, nullable=True)
