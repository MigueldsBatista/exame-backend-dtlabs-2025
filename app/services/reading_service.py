from sqlalchemy.orm import Session
from models.reading import Reading
from repository.reading_repository import ReadingRepository
from schemas.reading_schema import GetReadingParams


class ReadingService:
    def __init__(self, db: Session):
        self.reading_repository = ReadingRepository(db)
        
    def save(self, data: Reading) -> Reading:
        if not data:
            raise ValueError("No data provided")
        
        return self.reading_repository.save(data)
        

    def delete_by_id(self, id: int) -> None:
        entity = self.reading_repository.find_by_id(id)
        if not entity:
            raise ValueError(f"Reading with ID {id} not found")
        
        self.reading_repository.delete(entity)
                
    
    def find_all(self) -> list[Reading]:
        
        return self.reading_repository.find_all()
        

    def find_readings_by_params(self, filters: GetReadingParams) -> list[Reading] | None:
        
        if not filters:
            return self.find_all()

        if filters.aggregation:
            entities = self.reading_repository.find_aggregated_readings(filters)
            return entities if entities else []

        entities = self.reading_repository.find_by_criteria(filters)
        return entities if entities else []
    
    def find_by_server_ulid(self, server_ulid: str) -> list[Reading]:

        return self.reading_repository.find_by_server_ulid(server_ulid)