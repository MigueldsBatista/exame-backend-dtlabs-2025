from repository.base_repository import BaseRepository
from models.reading import Reading
from sqlalchemy.orm import Session

class ReadingRepository(BaseRepository[Reading]):
    """Repository for Reading model
    This repository handles the database operations for the Reading model."""

    def __init__(self, session: Session):
        """Initialize the repository with a database session."""
        super().__init__(Reading, session)

    def find_by_server_ulid(self, server_ulid: str):
        """Find readings by server ULID.
        
        Args:
            server_ulid (str): The unique identifier of the server.
        
        Returns:
            List[Reading]: A list of readings associated with the given server ULID.
        """
        return self.db.query(Reading).filter(Reading.server_ulid == server_ulid).all()

