from enum import Enum

class SensorType(Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    CURRENT = 'current'
    VOLTAGE = 'voltage'