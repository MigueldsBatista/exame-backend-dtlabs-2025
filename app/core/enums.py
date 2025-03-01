from enum import Enum

class AggregationType(Enum):
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'


class SensorType(Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    CURRENT = 'current'
    VOLTAGE = 'voltage'