from pydantic import BaseModel
from typing import Optional

class SensorSchema(BaseModel):
    _id: Optional[int]  # Sensor ID, Optional for creation (only returned after insertion)
    _name: str  # Sensor name (mandatory)
    _type: Optional[str] = None  # Sensor type, e.g., temperature, pressure
    _location: Optional[str] = None  # Sensor location
    _status: Optional[str] = 'active'  # Sensor status, default is 'active'

    class Config:
        orm_mode = True  # This makes the model work with SQLAlchemy models or ORM models
