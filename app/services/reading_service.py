from sqlalchemy.orm import Session
from repository.reading_repository import ReadingRepository
from schemas.reading_schema import PostReading, ReadingResponse

from mappers.reading_mapper import ReadingMapper

class ReadingService:
    """Service for Reading operations
    This service handles the business logic for Reading operations."""

    def __init__(self, db: Session):
        """Initialize the service with a database session."""
        self.reading_repository = ReadingRepository(db)
        
    def create_reading(self, data: PostReading) -> ReadingResponse:
        """Create a new reading.
        
        Args:
            data (PostReading): The data for the new reading.
        
        Returns:
            ReadingResponse: The created reading response.
        """
        entity = ReadingMapper.from_post_to_entity(data)
        self.reading_repository.save(entity)
        return ReadingMapper.from_entity_to_response(entity)

