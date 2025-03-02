from decimal import Decimal
from typing import List
from models.reading import Reading
from schemas.reading_schema import ReadingResponse, PostReading, GetReading

class ReadingMapper:


    @staticmethod
    def from_tuple_to_entity(entity: tuple, filters:GetReading) -> ReadingResponse:

        response = {
            "timestamp":entity[0],
            "temperature":entity[1] if filters.sensor_type=="temperature" or not filters.sensor_type else None,
            "humidity":entity[2] if filters.sensor_type=="humidity" or not filters.sensor_type else None,
            "current":entity[3] if filters.sensor_type=="current" or not filters.sensor_type else None,
            "voltage":entity[4] if filters.sensor_type=="voltage"or not filters.sensor_type  else None
        }
        return ReadingResponse(**response)


    @staticmethod
    def from_entity_to_response(entity: Reading, filters:GetReading=None) -> ReadingResponse:
        try:
            if not filters:
                return ReadingResponse(
                    server_ulid=entity.server_ulid,
                    temperature=entity.temperature,
                    humidity=entity.humidity,
                    current=entity.current,
                    voltage=entity.voltage,
                    timestamp=entity.timestamp_ms
                )
            
            if filters.aggregation:
                return ReadingResponse(
                    timestamp=entity.timestamp_ms,
                    temperature=entity.temperature if filters.sensor_type=="temperature" or not filters.sensor_type else None,
                    humidity=entity.humidity if filters.sensor_type=="humidity" or not filters.sensor_type else None,
                    current=entity.current if filters.sensor_type=="current" or not filters.sensor_type else None,
                    voltage=entity.voltage if filters.sensor_type=="voltage" or not filters.sensor_type else None
                )
            
            return ReadingResponse(
                server_ulid=entity.server_ulid,
                timestamp=entity.timestamp_ms,
                temperature=entity.temperature if filters.sensor_type=="temperature" or not filters.sensor_type else None,
                humidity=entity.humidity if filters.sensor_type=="humidity" or not filters.sensor_type else None,
                current=entity.current if filters.sensor_type=="current" or not filters.sensor_type else None,
                voltage=entity.voltage if filters.sensor_type=="voltage" or not filters.sensor_type else None
            )

        except AttributeError as e:
            # Se algum campo não for encontrado, levante um erro informativo
            raise AttributeError(f"Error in mapping entity to response: {str(e)}. Entity: {entity}")
        
    @staticmethod
    def from_post_to_entity(data: PostReading) -> Reading:
        return Reading(
            server_ulid=data.server_ulid,
            temperature=data.temperature,
            humidity=data.humidity,
            current=data.current,
            voltage=data.voltage,
            timestamp_ms=data.timestamp
        )

    
    def from_entities_to_responses(entities: List[Reading], filters=None) -> List[ReadingResponse]:
        return [ReadingMapper.from_entity_to_response(entity, filters) for entity in entities]
    
    def from_posts_to_entities(data: List[PostReading]) -> List[Reading]:
        return [ReadingMapper.from_post_to_entity(post) for post in data]
    
    def from_tuples_to_responses(entities: List[Reading], filters=None) -> List[ReadingResponse]:
        return [ReadingMapper.from_tuple_to_entity(entity, filters) for entity in entities]