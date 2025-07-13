from abc import ABC, abstractmethod
from datetime import datetime
import random
import numpy as np

class SensorGenerator(ABC):
    def __init__(self, noise_level: float = 0.0, threshold: float | None = None):
        self.noise_level = noise_level
        self.threshold = threshold

    @abstractmethod
    def generate_value(self, timestamp: datetime) -> float:
        """Generate a synthetic sensor value at a given time."""
        pass

    def add_noise(self, value: float) -> float:
        noise = np.random.normal(0, self.noise_level)
        return value + noise
