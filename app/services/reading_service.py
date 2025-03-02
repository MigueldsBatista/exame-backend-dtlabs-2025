from sqlalchemy.orm import Session
from models.reading import Reading
from repository.reading_repository import ReadingRepository
from schemas.reading_schema import GetReading, PostReading, ReadingResponse

from mappers.reading_mapper import ReadingMapper

class ReadingService:
    def __init__(self, db: Session):
        self.reading_repository = ReadingRepository(db)
        
    def save(self, data: PostReading) -> ReadingResponse:
        entity = ReadingMapper.from_post_to_entity(data)
        self.reading_repository.save(entity)
        return ReadingMapper.from_entity_to_response(entity)


    def delete_by_id(self, id: int) -> None:
        entity = self.reading_repository.find_by_id(id)
        if not entity:
            raise ValueError(f"Reading with ID {id} not found")
        
        self.reading_repository.delete(entity)
                
    
    def find_all(self, filters: GetReading = None) -> list[ReadingResponse]:
        
        if not filters:
            entities = self.reading_repository.find_all()
            return ReadingMapper.from_entities_to_responses(entities)

        entities = self.reading_repository.find_all(filters)

        return ReadingMapper.from_entities_to_responses(entities)
        

    def find_by_filters(self, filters: GetReading) -> list[ReadingResponse] | None:
        entities = self.reading_repository.find_by_filters(filters)

        if not entities:
            return []
        
        if isinstance(entities[0], Reading):
            return ReadingMapper.from_entities_to_responses(entities, filters)
        
        return ReadingMapper.from_tuples_to_responses(entities, filters)


    def find_by_server_ulid(self, server_ulid: str) -> list[ReadingResponse]:
        entities = self.reading_repository.find_by_server_ulid(server_ulid)
        return ReadingMapper.from_entities_to_responses(entities)