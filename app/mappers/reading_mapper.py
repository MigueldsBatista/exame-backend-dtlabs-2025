from typing import List
from models.reading import Reading
from schemas.reading_schema import ReadingResponse, PostReading, GetReadingParams

class ReadingMapper:


    @staticmethod
    def from_aggregate_tuple_to_response(entity: tuple, filters:GetReadingParams) -> ReadingResponse:

        response = {
            "timestamp":entity[0],
            "temperature":entity[1] if filters.sensor_type=="temperature" or not filters.sensor_type else None,
            "humidity":entity[2] if filters.sensor_type=="humidity" or not filters.sensor_type else None,
            "current":entity[3] if filters.sensor_type=="current" or not filters.sensor_type else None,
            "voltage":entity[4] if filters.sensor_type=="voltage"or not filters.sensor_type  else None
        }
        return ReadingResponse(**response)


    @staticmethod
    def from_entity_to_response(entity: Reading, filters:GetReadingParams=None) -> ReadingResponse:
        try:
            if not filters:
                return ReadingResponse(
                    server_ulid=entity.server_ulid,
                    temperature=entity.temperature,
                    humidity=entity.humidity,
                    current=entity.current,
                    voltage=entity.voltage,
                    timestamp=entity.timestamp
                )
            
            return ReadingResponse(
                server_ulid=entity.server_ulid if not filters.aggregation else None,
                timestamp=entity.timestamp,
                temperature=entity.temperature if filters.sensor_type=="temperature" or not filters.sensor_type else None,
                humidity=entity.humidity if filters.sensor_type=="humidity" or not filters.sensor_type else None,
                current=entity.current if filters.sensor_type=="current" or not filters.sensor_type else None,
                voltage=entity.voltage if filters.sensor_type=="voltage" or not filters.sensor_type else None
            )

        except AttributeError as e:
            raise AttributeError(f"Error in mapping entity to response: {str(e)}. Entity: {entity}")
        
    @staticmethod
    def from_post_to_entity(data: PostReading) -> Reading:
        return Reading(
            server_ulid=data.server_ulid,
            temperature=data.temperature,
            humidity=data.humidity,
            current=data.current,
            voltage=data.voltage,
            timestamp=data.timestamp
        )

    
    def from_entities_to_responses(entities: List[Reading], filters=None) -> List[ReadingResponse]:
        return [ReadingMapper.from_entity_to_response(entity, filters) for entity in entities]
    
    def from_posts_to_entities(data: List[PostReading]) -> List[Reading]:
        return [ReadingMapper.from_post_to_entity(post) for post in data]
    
    def from_aggregate_tuples_to_responses(entities: List[Reading], filters=None) -> List[ReadingResponse]:
        return [ReadingMapper.from_aggregate_tuple_to_response(entity, filters) for entity in entities]