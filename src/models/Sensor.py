from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Sensor(Base):
    __tablename__ = 'sensors'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    _name = Column(String(255), nullable=False)
    _type = Column(String(100))
    _location = Column(String(255))
    _status = Column(String(50), default='active')

    readings = relationship("Reading", back_populates="sensor")