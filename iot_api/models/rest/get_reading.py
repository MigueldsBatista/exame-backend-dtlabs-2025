from pydantic import BaseModel, field_validator
from typing import Optional
from models.aggregation_types import AggregationType
from models.sensor_types import SensorType

class GetReading(BaseModel):
    server_ulid: Optional[str]=None
    sensor_type: Optional[str]=None
    aggregation:Optional[str]=None

    @field_validator("sensor_type", mode="before")
    @classmethod
    def validate_aggregation(cls, value):
        if value is None:
            return value
        try:
            return SensorType(value)
        except ValueError:
            raise ValueError(f"Invalid sensor type: {value}")

    
    @field_validator("aggregation", mode="before")
    @classmethod
    def validate_aggregation(cls, value):
        if value is None:
            return value
        try:
            return AggregationType(value)
        except ValueError:
            raise ValueError(f"Invalid aggregation type: {value}")
