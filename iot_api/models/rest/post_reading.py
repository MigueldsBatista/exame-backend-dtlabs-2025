import iso8601
from pydantic import BaseModel, model_validator, root_validator
from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

class PostReading(BaseModel):
    server_ulid: str
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None

    
    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_reading(cls, data):
        # Verifica se é um dicionário (caso sim, estamos na validação inicial)
        if isinstance(data, dict):
            if all(data.get(field) is None for field in ("temperature", "humidity", "voltage", "current")):
                raise ValueError('At least one reading value must be provided')
        return data
    
    @field_validator('timestamp', mode='before')
    def parse_timestamp(cls, v):
        try:
            return iso8601.parse_date(v)
        except iso8601.ParseError:
            raise ValueError("timestamp must be in a valid ISO8601 format")
    
    @field_validator('humidity')
    def check_humidity(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('humidity must be between 0 and 100')
        return v