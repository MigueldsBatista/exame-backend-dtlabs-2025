from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from core.enums import SensorType, AggregationType
from datetime import datetime
import iso8601

class GetReadingParams(BaseModel):
    """Schema for retrieving reading data with optional filters
    This schema is used to structure the query parameters when retrieving reading data."""
    server_ulid: Optional[str] = None  # The unique identifier of the server
    sensor_type: Optional[str] = None  # The type of sensor
    aggregation: Optional[str] = None  # The type of aggregation
    start_time: Optional[datetime] = None  # The start time for the query
    end_time: Optional[datetime] = None  # The end time for the query

    @field_validator("sensor_type", mode="after")
    @classmethod
    def validate_sensor_type(cls, value):
        """Validator for sensor_type field
        This validator ensures that the sensor_type value is valid."""
        if value is None:
            return value
        try:
            sensor_value = SensorType(value)
            return sensor_value.value
        
        except ValueError as e:

            raise ValueError(f"Invalid sensor type: {value}") from e

    @field_validator("aggregation", mode="after")
    @classmethod
    def validate_aggregation(cls, value):
        """Validator for aggregation field
        This validator ensures that the aggregation value is valid."""
        if value is None:
            return value
        try:
            aggregation_value = AggregationType(value)
            return aggregation_value.value
        except ValueError as e:
            raise ValueError(f"Invalid aggregation type: {value}") from e

    @model_validator(mode='after')
    def validate_time_range(self):
        """Validate that start_time is before end_time when both are present"""
        if self.start_time is not None and self.end_time is not None:
            if self.start_time > self.end_time:
                raise ValueError("Start time cannot be after end time")
        return self

      

    def __str__(self):
        return f"GetReadingParams(server_ulid={self.server_ulid}, sensor_type={self.sensor_type}, aggregation={self.aggregation}, start_time={self.start_time}, end_time={self.end_time})"

#-----------------------------------------------------------------------

class PostReading(BaseModel):
    """Schema for posting a new reading
    This schema is used to validate the data when posting a new reading."""
    server_ulid: str  # The unique identifier of the server
    timestamp: datetime  # The timestamp of the reading
    temperature: Optional[float] = None  # The temperature reading
    humidity: Optional[float] = None  # The humidity reading
    voltage: Optional[float] = None  # The voltage reading
    current: Optional[float] = None  # The current reading

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_reading(cls, data):
        """Validator to ensure at least one reading value is provided"""
        if isinstance(data, dict):
            if all(data.get(field) is None for field in ("temperature", "humidity", "voltage", "current")):
                raise ValueError('At least one reading value must be provided')
        return data
    
    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, v):
        """Validator to parse and validate timestamp
        This validator ensures that the timestamp is in a valid ISO8601 format."""
        try:
            # Parse the string timestamp to datetime, then back to ISO8601 string if necessary
            str_timestamp = str(v)

            timestamp = iso8601.parse_date(str_timestamp)
            return timestamp.replace(tzinfo=None).isoformat()
        
        except iso8601.ParseError:
            raise ValueError("timestamp must be in a valid ISO8601 format")
    
    @field_validator('humidity')
    def check_humidity(cls, v):
        """Validator to check humidity range
        This validator ensures that the humidity value is between 0 and 100."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError('humidity must be between 0 and 100')
        return v
    

#-----------------------------------------------------------------------

class ReadingResponse(BaseModel):
    """Schema for reading response data
    This schema is used to structure the response data when querying reading information."""
    server_ulid: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float]  = None
    current: Optional[float] = None
    voltage: Optional[float] = None
    timestamp: datetime = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "exclude_unset": True
    }


    def __str__(self):
        return f"ReadingResponse(server_ulid={self.server_ulid}, temperature={self.temperature}, humidity={self.humidity}, current={self.current}, voltage={self.voltage}, timestamp={self.timestamp})"
    