from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class SensorReadingBase(BaseModel):
    timestamp: datetime
    machine_id: str
    temperature: Optional[float] = None
    vibration: Optional[float] = None
    pressure: Optional[float] = None
    power_consumption: Optional[float] = None

class SensorReadingCreate(SensorReadingBase):
    class Config:
        extra = "forbid"  

class SensorReadingRead(SensorReadingBase):
    id: UUID

    class Config:
        orm_mode = True
