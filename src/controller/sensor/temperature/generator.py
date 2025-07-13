import numpy as np
import random

from datetime import datetime

from src.controller.sensor.generator import SensorGenerator

from src.schemas.sensor.temperature.sensor_configuration import TemperatureConfiguration

from typing import Optional

class TemperatureSensorGenerator(SensorGenerator):
    def __init__(
        self,
        noise_level : Optional[float] = 0.5,
        threshold   : Optional[float] = 50.0,
        config: TemperatureConfiguration = TemperatureConfiguration()
    ):
        super().__init__(noise_level, threshold)
        self.config = config

    def generate_value(self, timestamp: datetime) -> float:
        hour = timestamp.hour

        if 0 <= hour < 8:
            mean, std = self.config.ranges["early_morning"]
        elif 8 <= hour < 16:
            mean, std = self.config.ranges["midday"]
        else:
            mean, std = self.config.ranges["evening"]

        base = np.random.normal(mean, std)
        value = self.add_noise(base)
        value = min(value, self.threshold)

        return round(value, 2)
