from models.reading import Reading
from schemas.reading_schema import ReadingResponse, PostReading

class ReadingMapper:

    @staticmethod
    def from_entity_to_response(entity: Reading) -> ReadingResponse:
        return ReadingResponse(
            id=entity.id,
            server_ulid=entity.server_ulid,
            temperature=entity.temperature,
            humidity=entity.humidity,
            current=entity.current,
            voltage=entity.voltage,
            timestamp=entity.timestamp_ms
        )

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



