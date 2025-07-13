from pydantic import BaseModel
from typing import Dict, Tuple


class TemperatureConfiguration(BaseModel):
    # Define temperature mean and stddev for each time range
    ranges: Dict[str, Tuple[float, float]] = {
        "early_morning": (22, 1.5),  # 0 <= hour < 8
        "midday": (30, 3.0),         # 8 <= hour < 16
        "evening": (26, 2.0)         # 16 <= hour < 24
    }