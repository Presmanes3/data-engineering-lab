from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReadingSchema(BaseModel):
    reading_id: Optional[int]  # Reading ID (Optional for creation, only returned after insertion)
    _id: int  # Sensor ID (Required, references the sensor)
    _value: float  # Measurement value (Required)
    _timestamp: Optional[datetime] = None  # Timestamp of the reading, default to current timestamp
    _unit: Optional[str] = None  # Unit of measurement (e.g., °C, psi)
    status: Optional[str] = 'valid'  # Reading status, default is 'valid'

    class Config:
        orm_mode = True  # This makes the model work with SQLAlchemy models or ORM models
