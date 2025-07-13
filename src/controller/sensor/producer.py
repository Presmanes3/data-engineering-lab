import datetime

import pandas as pd

from matplotlib import pyplot as plt

from src.controller.sensor.generator import SensorGenerator

from src.controller.sensor.temperature.generator import TemperatureSensorGenerator
from src.controller.time.timestamp_generator import TimestampGenerator

from src.schemas.sensor.reading import SensorReadingBase

from typing import List, Optional

from src.schemas.sensor.temperature.sensor_configuration import TemperatureConfiguration



class SensorProducer:
    def __init__(self, 
                 machine_id: str = "machine_1",
                 temperature_generator : Optional[SensorGenerator] = None,
                 vibration_generator: Optional[SensorGenerator] = None,
                 pressure_generator: Optional[SensorGenerator] = None,
                 power_consumption_generator: Optional[SensorGenerator] = None):
        
        self.machine_id = machine_id
        
        self.temperature_generator: Optional[SensorGenerator] = temperature_generator
        self.vibration_generator: Optional[SensorGenerator] = vibration_generator
        self.pressure_generator: Optional[SensorGenerator] = pressure_generator
        self.power_consumption_generator: Optional[SensorGenerator] = power_consumption_generator

    def generate_dataframe(self, start_hour: int, end_hour: int, interval_seconds: int) -> pd.DataFrame:
        timestamps = TimestampGenerator().get_timestamp_vector(start_hour, end_hour, interval_seconds)

        readings = []
        for timestamp in timestamps:
            reading = {"timestamp": timestamp}

            if self.temperature_generator is not None:
                reading["temperature"] = self.temperature_generator.generate_value(timestamp)
            if self.vibration_generator is not None:
                reading["vibration"] = self.vibration_generator.generate_value(timestamp)
            if self.pressure_generator is not None:
                reading["pressure"] = self.pressure_generator.generate_value(timestamp)
            if self.power_consumption_generator is not None:
                reading["power_consumption"] = self.power_consumption_generator.generate_value(timestamp)

            readings.append(reading)

        return pd.DataFrame(readings)

    def generate_readings(self,start_hour: int, end_hour: int, interval_seconds: int, date: datetime.date) -> List[SensorReadingBase]:
        timestamps = TimestampGenerator.get_timestamp_vector(start_hour, end_hour, interval_seconds, date)

        readings = []
        for timestamp in timestamps:
            reading_data = {"timestamp": timestamp}

            if self.temperature_generator is not None:
                reading_data["temperature"] = self.temperature_generator.generate_value(timestamp)
            if self.vibration_generator is not None:
                reading_data["vibration"] = self.vibration_generator.generate_value(timestamp)
            if self.pressure_generator is not None:
                reading_data["pressure"] = self.pressure_generator.generate_value(timestamp)
            if self.power_consumption_generator is not None:
                reading_data["power_consumption"] = self.power_consumption_generator.generate_value(timestamp)

            reading_data["machine_id"] = self.machine_id

            readings.append(SensorReadingBase(**reading_data))

        return readings


if __name__ == "__main__":

    temperature_configuration = TemperatureConfiguration(
        ranges={
            "early_morning": (22, 0.2),  # 0 <= hour < 8
            "midday": (30, 0.5),         # 8 <= hour < 16
            "evening": (26, 0.2)         # 16 <= hour < 24
        }
    )
    temperature_generator = TemperatureSensorGenerator(
        config = temperature_configuration
        )

    producer = SensorProducer(temperature_generator=temperature_generator)
    timestamp_gen = TimestampGenerator()

    df = producer.generate_dataframe(start_hour=5, end_hour=22, interval_seconds=60)
    
    plt.plot(df["timestamp"], df["temperature"])
    plt.xlabel("Timestamp")
    plt.ylabel("Temperature")
    plt.title("Temperature Readings")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    readings = producer.generate_readings(start_hour=5, end_hour=22, interval_seconds=60, date=datetime.date.today())
    print(f"Generated {len(readings)} sensor readings.")