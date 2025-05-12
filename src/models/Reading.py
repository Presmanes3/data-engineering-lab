from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Reading(Base):
    __tablename__ = 'readings'

    reading_id = Column(Integer, primary_key=True, autoincrement=True)
    _id = Column(Integer, ForeignKey('sensors._id', ondelete="CASCADE"))
    _value = Column(Numeric, nullable=False)
    _timestamp = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    _unit = Column(String(50))
    status = Column(String(50), default='valid')

    sensor = relationship("Sensor", back_populates="readings")